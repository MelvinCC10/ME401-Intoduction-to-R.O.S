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
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)
    turtlebot3_model = rospy.get_param("model", "burger")
    rate = rospy.Rate(10)

    time.sleep(2)


    try:

        print msg

        twist = Twist()

        

        twist.linear.x = 1.5; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)


    except:

        print e

    finally:

        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
