#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
from beginner_tutorials.msg import Position
import sys, select, os

if os.name == 'nt': # if windows
  import msvcrt
else:
  import tty, termios

def callback_ori(data, data_out):
	data_out.angular.roll  = data.angular.roll
	data_out.angular.pitch = data.angular.pitch
	data_out.angular.yaw   = data.angular.yaw

msg = """
Turtle Bot will move automatically
"""

e = """
Communications Failed
"""
kp = .035
des = 0
error = 0
coin = 0

if __name__=="__main__":

    position = Position()
    twist = Twist()

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('Move')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    turtlebot3_model = rospy.get_param("model", "burger")
    rospy.Subscriber('/eul', Position, callback_ori, (position))
    time.sleep(1)
    rate = rospy.Rate(10)

    try:

        print msg

        twist.linear.x = 0.5; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        time.sleep(2)

        while not rospy.is_shutdown():


            error = des - position.angular.yaw
            cmd = kp*error
            twist.linear.x = 0.5
            twist.angular.z = cmd
            pub.publish(twist)

            coin = coin + 1
            print(coin)

            #Step input
            if coin == 50:
                des = 90
                print(des)
            if coin == 100:
                des = 0
                print(des)

            rate.sleep()

    except:

        print e

    finally:

        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
