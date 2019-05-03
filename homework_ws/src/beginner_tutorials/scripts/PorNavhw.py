#!/usr/bin/env python
import rospy
import Dij
import numpy
import dubins
import csv
import matplotlib
import matplotlib.pyplot as plt
import time
import math
from geometry_msgs.msg import Twist
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler
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



def odom_callback(data):
	global odom, imu_data, yaw
	odom = data
	imu_data = data.pose.pose
	quat_list = [imu_data.orientation.x, imu_data.orientation.y, imu_data.orientation.z, imu_data.orientation.w]
	(roll, pitch, yaw) = euler_from_quaternion(quat_list)


msg = """
Turtle Bot will move automatically
"""

e = """
Communications Failed
"""
N = 1
kp = .02
des = 0
error = 0
low_limt = -2.800000
high_limit = 2.800000
coin = 0
end = False
tol = .1
num_wraps = 0
threshold = 30
olddes = 0


if __name__=="__main__":

    position = Position()
    twist = Twist()

    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('Move')
    #sets publisher for tb2
    pub = rospy.Publisher('/tb2/cmd_vel', Twist, queue_size=10)
    pub1 = rospy.Publisher('/tb1/cmd_vel', Twist, queue_size=10)
    turtlebot3_model = rospy.get_param("model", "burger")

    #gets yaw of tb2
    rospy.Subscriber('/eul', Position, callback_ori, (position))
    #gets yaw of tb1
    #rospy.Subscriber('/eul1', Position, callback_ori, (position))

    #gets location information from both bots
    rospy.Subscriber("/tb1/odom",Odometry,odom_callback)
    rospy.Subscriber('/tb2/odom', Odometry, callback_pos, (position))



    time.sleep(1)
    rate = rospy.Rate(10)



    try:
#####################################################################
        print msg
        waypoints =  Dij.findShortPath(10,[2,1],[7,2],[(5,0), (5,1), (5,2), (5,3), (5,4), (1,4), (2,3), (3,2), (3,3)])#
        print waypoints
        turning_radius = .001
        step_size = 0.5
        wpm = []

        print "1"
        # for each item in waypoints list
        for i in range(len(waypoints)):

            #Set current point to current iteration index ie. iteration 0 use index 0 waypoints
            q0 = waypoints[i]

            #if next point to index (current iteration + 1) is True
            try:
                q1 = waypoints[i+1]
                print "2"
            except:
                break
                # next point  = index (current iteration + 1)
            #else
                #break
            #set q1, q2
            #find path from current point to next point
            print "here"
            path = dubins.shortest_path(q0, q1, turning_radius)
            configurations, _ = path.sample_many(step_size)
            # add all points to end of master list
            print "2"
            for i in range(len(configurations)):
                wpm.append(configurations[i])
            print configurations
            print len(configurations)
            print "3"
        setx = []
        sety = []
        for i in range(len(wpm)):
            setx.append(wpm[i][0])
            sety.append(wpm[i][1])

        print "x"
        print setx
        print "y"
        print sety

        print "here"
        plt.plot(setx, sety)
        plt.grid()
        plt.show()
        print "here"
        wp = wpm[coin]
        #print wpm

        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        pub1.publish(twist)
        time.sleep(2)
        oldLos = 0
#####################################################################
        ex = []
        ey = []
        cx = []
        cy = []


        while not rospy.is_shutdown():

            #Getting Location of boths bots
            cur_pose = odom.pose.pose.position
            cur_loc = cur_pose.x, cur_pose.y
            x = position.linear.x
            y = position.linear.y
            cur_loc2 = x, y
            print "here"
            ##################################################################
            # check current pose
            x1 = cur_pose.x
            y1 = cur_pose.y
            ex.append(x1)
            ey.append(y1)
            cx.append(x)
            cy.append(y)


            ##################################################################
            twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0



            #ProNav done here
            print position.angular.yaw
            LOS = 0-(math.atan2((cur_pose.y-y),(cur_pose.x-x)) * (180/3.14))
            cmd = -N*(LOS-oldLos)*10


            twist.linear.x = 0.2; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = cmd
            pub.publish(twist)
            oldLos = LOS

            if len(ex) > 450:
                break

            rate.sleep()


    except:

        print e

    finally:

        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

        new_list = zip(ex, ey)
        with open('Ep2_1000p.csv', 'wb+') as csvfile:
             filewriter = csv.writer(csvfile)
             filewriter.writerows(new_list)
        print "wrote"

        new_list = zip(cx, cy)
        with open('Cp2_1000p.csv', 'wb+') as csvfile:
             filewriter = csv.writer(csvfile)
             filewriter.writerows(new_list)
        print "wrote"

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
