#!/usr/bin/env python
import rospy
import numpy
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
WayPoint
"""

e = """
Communications Failed
"""
kp = .02
des = 0
error = 0
low_limt = -.800000
high_limit = .800000
coin = 0
end = False
tol = .1


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


        waypoints = [[0,0, 0], [0,1, 0], [2,2, 90], [3, -3,-90]]
        turning_radius = .3
        step_size = 0.5
        wpm = []
        # for each item in waypoints list
        for i in range(len(waypoints)):
            #Set current point to current iteration index ie. iteration 0 use index 0 waypoints
            q0 = waypoints[i]
            #if next point to index (current iteration + 1) is True
            try:
                q1 = waypoints[i+1]
            except:
                break
                # next point  = index (current iteration + 1)
            #else
                #break
            #set q1, q2
            #find path from current point to next point
            path = dubins.shortest_path(q0, q1, turning_radius)
            configurations, _ = path.sample_many(step_size)
            # add all points to end of master list
            for i in range(len(configurations)):
                wpm.append(configurations[i])
            print configurations
            print len(configurations)

        setx = []
        sety = []
        for i in range(len(wpm)):
            setx.append(wpm[i][0])
            sety.append(wpm[i][1])


        plt.plot(setx, sety)
        plt.grid()
        plt.show()






        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)
        time.sleep(2)


        #set waypoint to first way WayPoint
        wp = wpm[coin]
        print wpm


        while not rospy.is_shutdown():



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
                    wp = wpm[coin]
                    if not wpm[coin]:
                        twist.linear.x = 0
                        end = True
                        break


            error = des - position.angular.yaw
            print error


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

        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
