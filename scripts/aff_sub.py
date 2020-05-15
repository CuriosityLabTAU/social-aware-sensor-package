#! /usr/bin/python
import rospy
import matplotlib.pyplot as plt
import time
from std_msgs.msg import String
from affdex_msgs.msg import AffdexFrameInfo
from std_msgs.msg import Int32

new_data = str()
start_time = time.time()
faces = {}
plots = {}
pub = rospy.Publisher("/send_data", String, queue_size=1)
pub2 = rospy.Publisher("/send_speaker_data", String, queue_size=1)


def callback_affdex_data(msg):
    global new_data, faces, plots, pub
    face_index = len(faces)
    x_now = msg.face_points[26].x
    look_at_x = (((x_now + 640) % 1280) + (2*msg.measurements[1]*(1280/360))) % 1280
    look_at_person = "0"

    for index, timeline in faces.items():
        if timeline[0]['X'] > x_now - 70 and timeline[0]['X'] < x_now + 70:
            face_index = index
            timeline[0]['X'] = x_now

            break
    for index, face in faces.items():
        if look_at_x > face[0]['X'] - 100 and look_at_x < face[0]['X'] + 100:
            look_at_person = index+1

    if face_index not in faces:
        faces[face_index] = []

    times = time.time() - start_time

    personality = {}
    personality["Time"] = times
    personality["Joy"] = round(msg.emotions[0], 2)
    personality["X"] = x_now
    personality["Look_At"] = look_at_x
    personality["Look_at_Person"] = look_at_person

    faces[face_index].append(personality)

    new_data = "time:" + str(times) + " " + "PersonID:" + str(face_index+1) + " " + "Location:" + str(msg.face_points[26].x) + " " + "LookAt:" + str((((x_now + 640) % 1280) + (2*msg.measurements[1]*(1280/360))) % 1280) + " " + "LookAtPerson:" + str(look_at_person) + " " + "Joy:" + str(msg.emotions[0]) + " " + "Anger:" + str(msg.emotions[1]) + " " + "Didgust:" + str(msg.emotions[2]) + " " + "Contempt:" + str(msg.emotions[3]) + " " + "Engagement:" + str(msg.emotions[4]) + " " + "Fear:" + str(msg.emotions[5]) + " " + "Sadness:" + str(msg.emotions[6]) + " " + "Yaw:" + str(msg.measurements[1]) + " " + "Roll:" + str(msg.measurements[2]) + " " + "Pitch:" + str(msg.measurements[3]) + " " + "Surprise:" + str(msg.emotions[7]) + " " + "Valence:" + str(msg.emotions[8]) + " " + "Nose Tip:(" + str(msg.face_points[12].x) + "," + str(msg.face_points[12].y) + ") " + "Chin:(" + str(msg.face_points[2].x) + "," + str(msg.face_points[2].y) + ") " + "RightEyeOuter:(" + str(msg.face_points[16].x) + "," + str(msg.face_points[16].y) + ") " + "RightEyeInner:(" + str(msg.face_points[17].x) + "," + str(msg.face_points[17].y) + ") " + "LeftEyeInner:(" + str(msg.face_points[18].x) + "," + str(msg.face_points[18].y) + ") " + "LeftEyeOuter:(" + str(msg.face_points[19].x) + "," + str(msg.face_points[19].y) + ") " + "RightLip_Corener:(" + str(msg.face_points[20].x) + "," + str(msg.face_points[20].y) + ") " + "LeftLipCorner:(" + str(msg.face_points[24].x) + "," + str(msg.face_points[24].y) + ")"

    print('Affdex published')
    pub.publish(new_data)


def respeaker_callback(msg):
    global pub
    x_talk = str(msg)
    x_talk = x_talk[6:]
    x_talk = int(x_talk)
    for index, face in faces.items():
        if x_talk > face[0]['X'] - 60 and x_talk < face[0]['X'] + 60:
            person_is_speaking = index+1
            #str_respeaker = "Person:" + str(person_is_speaking) + " X = " + str(x_talk) + " In time: " + str(time.time() - start_time)
            str_respeaker = '{"person_id":%s,"x":%s,"time":%s}' % (person_is_speaking, x_talk, time.time() - start_time)
            pub2.publish(str_respeaker)


def main():
    rospy.init_node('affdex_data_edit', anonymous=True)
    rospy.Subscriber("/affdex_data", AffdexFrameInfo, callback_affdex_data)
    rospy.Subscriber("/ReSpeaker", Int32, respeaker_callback)
    r = rospy.Rate(3)
    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
