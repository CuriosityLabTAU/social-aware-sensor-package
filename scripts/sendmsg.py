#! /usr/bin/python
import rospy
from std_msgs.msg import String

def main():
    rospy.init_node('send_messenger', anonymous=True)
    pub = rospy.Publisher("/send_msg", String, queue_size=1)
    r = rospy.Rate(3)

    while not rospy.is_shutdown():
        print "Type 'C' for Clearing Look-At Matrix"
        print "Type 'R' for Clearing Speaking Matrix \n"
        command_input = raw_input()
        if command_input == 'C':
            pub.publish("C")
            print("\nClearing Look At Matrix... \n")
        if command_input == 'R':
            pub.publish("R")
            print("\nClearing Talking Persons... \n")
        r.sleep()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
