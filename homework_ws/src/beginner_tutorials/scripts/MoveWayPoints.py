#!/usr/bin/env python
import rospy
import time
import math
from geometry_msgs.msg import Twist
from beginner_tutorials.msg import Position
import sys, select, os

if os.name == 'nt': # if windows
  import msvcrt
else:
  import tty, termios

def callback_pos(data, data_out):
	data_out.linear.x = data.pose.pose.position.x
	data_out.linear.y = data.pose.pose.position.y
	data_out.linear.z = data.pose.pose.position.z

def callback_ori(data, data_out):
	data_out.angular.roll  = data.angular.roll
	data_out.angular.pitch = data.angular.pitch
	data_out.angular.yaw   = data.angular.yaw

def check(value,wp):
    if (wp - tol) <= value <= (wp + tol) and round(value,2)==value:
        return True
    return False

msg = """
Turtle Bot will move automatically
WayPoint
"""

e = """
Communications Failed
"""
kp = .035
des = 0
error = 0
low_limt = -.5
high_limit = .5
coin = 0
end = False

waypoints =[[0,0], [0,1], [2,2], [3, -3]]


if __name__=="__main__":

    position = Position()
    twist = Twist()

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('Move')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    turtlebot3_model = rospy.get_param("model", "burger")

    rospy.Subscriber('/eul', Position, callback_ori, (position))
    rospy.Subscriber('/odom', Odometry, callback_pos, (position))

    time.sleep(1)
    rate = rospy.Rate(100)

    try:

        print msg

        twist.linear.x = 0.5; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        time.sleep(2)

        #set waypoint to first way WayPoint
        wp = waypoints[0]

        while not rospy.is_shutdown():


            # check current pose
            x = position.linear.x
            y = position.linear.y

            # if not withen a spec range of waypoint
            if not check(x,wp[0]) and check(y,wp[1]):
                #change heading twords WayPoint
                des = atan2(wp[1]-y,wp[0]-x)
                twist.linear.x = .2
            else:
                if end = False
                    coin = coin +1
                    if not waypoints[coin+1]:
                        twist.linear.x = 0
                        end = True
                        break
                    wp = waypoints[coin + 1]

            error = des - position.angular.yaw
            cmd = kp*error

            if cmd > high_limit:
                cmd = high_limit
            if cmd < low_limt:
                cdm = low_limt

            twist.linear.x = 0.5
            twist.angular.z = cmd
            pub.publish(twist)
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
