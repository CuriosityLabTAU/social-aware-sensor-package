#!/usr/bin/env python
import rospy
from subprocess import Popen, PIPE
from std_msgs.msg import Int32

sudo_password = '1234567'
command = 'python microphone_tuning.py'.split()


def read_microphone():
    p = Popen(['sudo', '-S'] + command, stdin=PIPE, stderr=PIPE, universal_newlines=True, stdout=PIPE)
    (output, error) = p.communicate(sudo_password + '\n')
    return output


def respeaker():
    pub = rospy.Publisher('ReSpeaker', Int32, queue_size=1)
    rospy.init_node('ReSpeaker_Pub', anonymous=True)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            str_mic = read_microphone()
            if len(str_mic) > 0: # nothing is recieved
                direction_str = int(str_mic)
                pub.publish(direction_str)
                print(direction_str)
        except KeyboardInterrupt:
            break
        rate.sleep()


if __name__ == '__main__':
    try:
        respeaker()
    except rospy.ROSInterruptException:
        print "Turn on Microphone"
        pass

