import subprocess
import time


def main():
    try:
        #chose 1 for camera and 0 for rosbag
        camera_or_rosbag = 1
        # chose 1 for Microphone ON and 0 for Microphone OFF
        microphone_mode = 1

        process1 = subprocess.Popen("roslaunch multi_camera_affdex multi_camera_affdex.launch", shell=True)
        # Affectiva subproces1
        time.sleep(1)
        #waiting for affactiva

        process2 = subprocess.Popen("python aff_sub.py",  shell=True)
        #subscriber to affectiva and respeaker, publish all data to "/omer_data"
        process25 = subprocess.Popen("python conc.py", shell=True)
        # subscriber to /omer_data publish all data to "/omer_conc"

        if camera_or_rosbag == 1:
            process3 = subprocess.Popen("rosbag record -O ../output/last_record.bag /usb_cam/image_raw", shell=True)
            process4 = subprocess.Popen("python face_publisher.py", shell=True)
            if microphone_mode == 1:
                process5 = subprocess.Popen("rosbag record -O microphone.bag /ReSpeaker", shell=True)
                process6 = subprocess.Popen("python curious_microphone.py", shell=True)

        elif camera_or_rosbag == 0:
            process3 = subprocess.Popen("rosbag play last_record.bag", shell=True)
            if microphone_mode == 0:
                process4 = subprocess.Popen("rosbag play microphone.bag", shell=True)

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        process1.kill()
        process2.kill()
        process25.kill()
        process3.kill()
        process4.kill()
        if camera_or_rosbag == 1 and microphone_mode == 1:
            process5.kill()
            process6.kill()
        print("Program has stopped ...\n")
        exit()

if __name__ == '__main__':
    main()
