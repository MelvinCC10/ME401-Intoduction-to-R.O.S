#!/usr/bin/env python
import rospy
import time
import math
from geometry_msgs.msg import Twist
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry
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
tol = .2

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

        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        time.sleep(2)


        #set waypoint to first way WayPoint
        wp = waypoints[coin]


        while not rospy.is_shutdown():

            print wp
            print "1"

            # check current pose
            x = position.linear.x
            y = position.linear.y
            print "2"

            # if not withen a spec range of waypoint
            if not ((wp[0] - tol) <= x <= (wp[0] + tol)) or not ((wp[1] - tol) <= y <= (wp[1] + tol)):
                #change heading twords WayPoint
                des = math.atan2((wp[1]-y),(wp[0]-x)) * (180/3.14)
                #twist.linear.x = 0
            else:
                if end == False:

                    coin = coin +1
                    print coin
                    wp = waypoints[coin]
                    if not waypoints[coin]:
                        twist.linear.x = 0
                        end = True
                        break


            error = des - position.angular.yaw
            print error


            if 1 >= error:
                twist.linear.x = .2

            cmd = kp*error

            if cmd > high_limit:
                cmd = high_limit
            if cmd < low_limt:
                cdm = low_limt


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
