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

msg = """
Dubins is generating path
"""

msg2 = """
Dubins path has been generated
"""

e = """
Communications Failed
"""

waypoints = [[0,0, 90], [0,1, 0], [2,2, 90], [3, -3,-90]]
turning_radius = 1.0
step_size = 0.5
wp = []

if __name__=="__main__":

    position = Position()
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('Dubins')
    #pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    rate = rospy.Rate(100)


    try:

        while not rospy.is_shutdown():

            # for each item in waypoints list
            for i in range(len(waypoints)):
                print i
                #Set current point to current iteration index ie. iteration 0 use index 0 waypoints
                q0 = waypoints[i]
                #if next point to index (current iteration + 1) is True
                if not waypoints[i+1]:
                    break
                else:
                    q1 = waypoints[i+1]
                    # next point  = index (current iteration + 1)
                #else
                    #break
                #set q1, q2
                #find path from current point to next point
                path = dubins.shortest_path(q0, q1, turning_radius)
                configurations, _ = path.sample_many(step_size)
                print configurations
                print "next"
                # add all points to end of master list
                for i in range(len(configurations)):
                    wp.append(configurations[i])



    except:

        print e

    finally:

        print e
        print wp
        print len(wp)
