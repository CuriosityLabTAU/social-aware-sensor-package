#! /usr/bin/python
import rospy
from std_msgs.msg import String
import json

pubcamera = rospy.Publisher("/conc_camera", String, queue_size=1)
pubspeaker = rospy.Publisher("/conc_speaker", String, queue_size=1)
who_look_at_who = {}
who_look_at_who_mat = [[0]]
persons = ['0']
talking_persons = [0]
talking_persons_x = [0]
talking_output = [0]
def callback_conc_data(msg):
    global who_look_at_who

    #matrix of who looking at who
    names = str(msg).split(" ")
    person_id = (names[2].split(":"))[1]
    look_at_person = (names[5].split(":"))[1]


    if person_id not in persons:
        persons.append(person_id)
        for row in who_look_at_who_mat:
            row.append(0)
        who_look_at_who_mat.append([0]*len(persons))
        who_look_at_who_mat[-1][int(look_at_person)] = 1
    else:
        who_look_at_who_mat[int(person_id)][int(look_at_person)] += 1

    pubcamera.publish(str(who_look_at_who_mat))

def callback_msg(msg):
    print('======= send msg', str(msg))
    if str(msg)[-1] == 'C':
        for person in range(len(who_look_at_who_mat)):
            for index in range(len(persons)):
                who_look_at_who_mat[person][index] = 0
    elif str(msg)[-1] == 'R':
        for person in range(len(talking_persons)):
            talking_persons[person] = 0



def callback_ReSpeaker_msg(msg):
    d = json.loads(str(msg)[6:])
    if len(talking_persons) <= d['person_id']:
        talking_persons.append(0)
        talking_persons_x.append(0)
        talking_output.append(0)
    talking_persons[d['person_id']] += 1
    talking_persons_x[d['person_id']] = d['x']
    talking_output[d['person_id']] = "%s_%s" % (str(talking_persons_x[d['person_id']]), str(talking_persons[d['person_id']]))
    pubspeaker.publish(str(talking_output))



def main():
    rospy.init_node('make_conclusion', anonymous=True)
    rospy.Subscriber("/send_msg", String, callback_msg)
    rospy.Subscriber("/send_data", String, callback_conc_data)
    rospy.Subscriber("/send_speaker_data", String, callback_ReSpeaker_msg)
    r = rospy.Rate(3)
    while not rospy.is_shutdown():
        r.sleep()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass

