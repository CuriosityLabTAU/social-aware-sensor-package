#!/usr/bin/env python
from tuning import Tuning
import usb.core
import usb.util
import rospy
from std_msgs.msg import Int32

dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)

def respeaker():
    global dev
    pub = rospy.Publisher('ReSpeaker', Int32, queue_size=1)
    rospy.init_node('ReSpeaker_Pub', anonymous=True)
    mic_tuning = Tuning(dev)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        try:
            if mic_tuning.is_voice() == 1:
                direction_str = (360-mic_tuning.direction)*1280/360
                pub.publish(direction_str)
        except KeyboardInterrupt:
            break
        rate.sleep()


if __name__ == '__main__':
    try:
        respeaker()
    except rospy.ROSInterruptException:
        print "Turn on Microphone"
        pass
