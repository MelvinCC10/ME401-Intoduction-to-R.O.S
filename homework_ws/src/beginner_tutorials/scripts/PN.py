#!/usr/bin/env python
import rospy
import time
from geometry_msgs.msg import Twist
import sys, select, os

if os.name == 'nt': # if windows
  import msvcrt
else:
  import tty, termios


msg = """
This is the proptional naviagtion
"""

e = """
Communications Failed
"""

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('PN')
    pub = rospy.Publisher('/tb2/cmd_vel', Twist, queue_size=10)
    turtlebot3_model = rospy.get_param("model", "burger")
    rate = rospy.Rate(10)
    time.sleep(2)


    try:

        print msg

        twist = Twist()
        while not rospy.is_shutdown():

            #ProNav done here
            print position.angular.yaw
            LOS = 0-(math.atan2((cur_pose.y-y),(cur_pose.x-x)) * (180/3.14))
            cmd = -N*(LOS-oldLos)


            twist.linear.x = 0.2; twist.linear.y = 0.0; twist.linear.z = 0.0
            twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = cmd
            pub.publish(twist)
            oldLos = LOS



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
