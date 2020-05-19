#!/usr/bin/env python
import rospy
import cv2
import numpy as np
import subprocess
import logging
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from threading import Thread
import pyscreenshot as ImageGrab
import threading


image = None
input_device = open('sensor_type.txt', 'r').read()


def find_devices():
    devices_ = {}
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        ret, frame = cap.read()
        if not ret:
            break
        else:
            print(index, frame.shape)
            devices_[index] = frame.shape

        cap.release()
        index += 1
    print('**** devices ****')
    print(devices_)
    # find 360
    for i, d in devices_.items():
        if d[1] == 1280:
            return i
    return devices_.keys()[0]


def thread1_take_pictures():
    # this function takes pictures
    # each picture is saved to VideoWriter and display in a new window
    # In additional, the last picture taken will be saved on global variable named "last_picture"

    global image

    subprocess.call("./projection -x fisheye_grid_xmap.pgm -y fisheye_grid_ymap.pgm -h 640 -w 1280 -r 640 -c 1280 -b 33 -m thetas", shell=True)
    # create the mapping files from dualfisheye to rectungaular -h 640 -w 1280 -r 640 -c 1280 -b 29  or 960 1920 960 1920 51

    #out = cv2.VideoWriter('outpy.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 2, (1280, 640))
    the_device = find_devices()
    print(the_device)
    cap = cv2.VideoCapture(the_device)


    try:
        while True:
            ret, frame = cap.read()

            crop_img = frame[0:640, 0:1280]
            # read & cut the unrellavnt data from the image - always 640 and 1280!!!!!

            # resize_img = cv2.resize(crop_img, (1920, 960))
            # resize the image for resolution 1920:960

            cv2.imwrite('captured.png', crop_img)
            # save the image for ffmpeg

            ffmpeg_process = subprocess.Popen("ffmpeg -y -i captured.png -i fisheye_grid_xmap.pgm -i fisheye_grid_ymap.pgm -filter_complex remap fixed.png", shell=True)
            # remapping the image from fisheye to  equirectangular
            ffmpeg_process.communicate()
            # wait until the process is ending

            image2 = cv2.imread('fixed.png')
            # image2 = cv2.imread('captured.png')
            # read the equirectangular image

            image = image2
            # in order to use the image in the other thread too we put it in a global variable

            cv2.imshow('Live', image2)
            k = cv2.waitKey(1)
            # display live

            # out.write(image2)
            # recording for video

            if k == ord('q'):
                cap.release()
                cv2.destroyAllWindows()

    except:
        print logging.exception("thread1_take_pictures exception")
        print "Please Turn on Camera or plug it in"

    cap.release()
    cv2.destroyAllWindows()


def thread2_take_pictures():
    global image

    while(True):
        image2 = ImageGrab.grab()
        image = np.array(image2)
        image2.save('fixed.png')
        threading._sleep(0.5)


def rospy_main_thread():
    # this function takes the pending "last_picture"
    # it detect and crop faces and publish them to "/usb_cam/image_raw" topic which Affectiva will subscribe too and analyze
    # later Affectiva will send the data to a "/affdex_data" topic which will be acquired by plot_sub
    global image

    def faces_detection(image2):
        cascPath = "haarcascade_frontalface_alt2.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        gray = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.125,
            minNeighbors=5,
            minSize=(2, 2),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        print("Found {0} faces!".format(len(faces)))
        return faces

    pub = rospy.Publisher('/usb_cam/image_raw', Image, queue_size=1)
    img_pub = rospy.Publisher('/full_image', Image, queue_size=1)
    rospy.init_node('Camera_Publisher', anonymous=True)

    rate = rospy.Rate(40)  # 10hzro
    bridge = CvBridge()

    while not rospy.is_shutdown():

        if image is None:
            continue
        image2 = image
        img_pub.publish(bridge.cv2_to_imgmsg(image2, "bgr8"))
        image = None

        found_faces = faces_detection(image2)

        for (x, y, w, h) in found_faces:
            # publish face each time face is recognized
            # send some more of the information of each face for the affectiva to read it with better chance
            if x > 30 and (1280 - (x + w)) > 30 and y > 30 and (640 - (y + h)) > 30:
                cropped_face = image2[(y - 30): (y + h + 30), (x - 30):(x + w + 30)]
                black_blank = np.zeros((h + 60, (x - 30), 3), np.uint8)
            else:
                cropped_face = image2[y:y+h, x:x + w]
                black_blank = np.zeros((h, x, 3), np.uint8)

            black_blank[:] = (0, 0, 0)
            ready = np.concatenate((black_blank, cropped_face), axis=1)
            cv2_frame = np.asarray(ready)

            image_message = bridge.cv2_to_imgmsg(cv2_frame, "bgr8")

            try:
                pub.publish(image_message)  # publishing the faces images
            except CvBridgeError as e:
                print(e)
            rate.sleep()


def main():
    try:
        if 'camera' in input_device:
            f = Thread(target=thread1_take_pictures)
        elif 'zoom' in input_device:
            f = Thread(target=thread2_take_pictures)
        else:
            f = None

        if f:
            f.daemon = True
            f.start()
        rospy_main_thread()
    except:
        print("not publishing")


if __name__ == '__main__':
    main()
