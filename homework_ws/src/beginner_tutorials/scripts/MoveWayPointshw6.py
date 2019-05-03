#!/usr/bin/env python
import rospy
import RRT_hw
import numpy
import csv
import dubins
import matplotlib
import matplotlib.pyplot as plt
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
WayPoint test
"""

e = """
Communications Failed
"""
kp = .02
des = 0
error = 0
low_limt = -8.800000
high_limit = 8.800000
coin = 0
end = False
tol = .1
num_wraps = 0
threshold = 30
olddes = 0


#waypoints =[[0,0], [0,1], [2,2], [3, -3]]


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


        waypoints =  RRT_hw.RRT([10,10],[0,0],[1,9],[[1,1], [4,4], [3,4], [5,0], [5,1], [0,7], [1,7], [2,7], [3,7]])
        print waypoints
        turning_radius = .001
        step_size = 0.5
        wpm = waypoints
        print 'here'









        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        time.sleep(2)


        #set waypoint to first way WayPoint
        wp = wpm[coin]
        print wpm

        ex = []
        ey = []

        while not rospy.is_shutdown():




            # check current pose
            x = position.linear.x
            y = position.linear.y
            ex.append(x)
            ey.append(y)


            # if not withen a spec range of waypoint
            if not ((wp[0] - tol) <= x <= (wp[0] + tol)) or not ((wp[1] - tol) <= y <= (wp[1] + tol)):
                #change heading twords WayPoint
                des = math.atan2((wp[1]-y),(wp[0]-x)) * (180/3.14)
                print des

                if olddes < -threshold and des > threshold: # from -pi to pi (increasing negative)
            		num_wraps = num_wraps - 1
            	elif olddes > threshold and des < -threshold:
            		num_wraps = num_wraps + 1

                olddes = des
                des = des + 360 * num_wraps



            else:
                if end == False:

                    coin = coin +1
                    print coin
                    wp = wpm[coin]
                    if not wpm[coin]:
                        twist.linear.x = 0
                        end = True
                        break


            error = des - position.angular.yaw



            #if 1 >= error:
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

        new_list = zip(ex, ey)
        with open('p2_hw6.csv', 'wb+') as csvfile:
             filewriter = csv.writer(csvfile)
             filewriter.writerows(new_list)
        print "wrote"

        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
