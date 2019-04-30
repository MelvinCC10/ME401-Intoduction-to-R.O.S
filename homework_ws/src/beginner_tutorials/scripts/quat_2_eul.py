#!/usr/bin/env python
import rospy, math
import os
clear = lambda : os.system('clear')

from nav_msgs.msg import Odometry
# this package is used for the actual quat to eul transformation
from tf.transformations import euler_from_quaternion, quaternion_from_euler
# this imports the custom message format
from beginner_tutorials.msg import Position

msg0 = """
quat to eul is running
"""
msg1 = """
quat to eul is running.
"""
msg2 = """
quat to eul is running..
"""
msg3 = """
quat to eul is running...
"""
msg4 = """
quat to eul is running....
"""

coin = 0

# create the globals old_yaw and num_wraps and instantiate with values of 0
old_yaw = 0
num_wraps = 0

# this function will be used as the callback for a subscriber to the /odom topic
def get_rotation (msg, pub):

	# establish a threshold for the wrap counter, in this case the threshold is 15 degrees
	# but the value must be converted to radians for use on the angles directly
	threshold = 15*math.pi/180

	# create a blank object of type Position()
	pos_msg = Position()

	# in python use of the "global" keyword inside a function indicates that use of the
	# specified variable names within that function should refer to the global instance
	# of variables with that same name, in this case within the function get_rotation
	# anytime we use "roll","pitch","yaw","wrapped_yaw","old_yaw","num_wraps" we are
	# referring to the global variables with these names (these variables are defined
	# at the global scope, outside of the calling function)
	global roll, pitch, yaw, wrapped_yaw, old_yaw, num_wraps

	# the following code is copied from an example on converting quaternions to euler angles
	# source:
	# http://www.theconstructsim.com/ros-qa-how-to-convert-quaternions-to-euler-angles/
	orientation_q = msg.pose.pose.orientation
	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
	(roll, pitch, yaw) = euler_from_quaternion (orientation_list)

	# the following block catches the yaw discontinuity and increments the wrap counter
	# valid yaw range is from -pi to pi
	if old_yaw < -threshold and yaw > threshold: # from -pi to pi (increasing negative)
		num_wraps = num_wraps - 1
	elif old_yaw > threshold and yaw < -threshold:
		num_wraps = num_wraps + 1

	# establish the new value of wrapped_yaw using the updated num_wraps
	wrapped_yaw = yaw + 2*math.pi*num_wraps

	# update old_yaw, this variable is used in the wrap catch block
	old_yaw = yaw

	# write the converted angles to the angular properties of the position message
	# also convert the radian positions to degrees
	pos_msg.angular.roll  = roll * 180/math.pi
	pos_msg.angular.pitch = pitch * 180/math.pi
	pos_msg.angular.yaw   = wrapped_yaw * 180/math.pi

	# make sure we publish the message
	pub.publish(pos_msg)

# this function will be used as the callback for a subscriber to the /odom topic
def get_rotation1 (msg, pub):

	# establish a threshold for the wrap counter, in this case the threshold is 15 degrees
	# but the value must be converted to radians for use on the angles directly
	threshold = 15*math.pi/180

	# create a blank object of type Position()
	pos_msg = Position()

	# in python use of the "global" keyword inside a function indicates that use of the
	# specified variable names within that function should refer to the global instance
	# of variables with that same name, in this case within the function get_rotation
	# anytime we use "roll","pitch","yaw","wrapped_yaw","old_yaw","num_wraps" we are
	# referring to the global variables with these names (these variables are defined
	# at the global scope, outside of the calling function)
	global roll1, pitch1, yaw1, wrapped_yaw1, old_yaw1, num_wraps1

	# the following code is copied from an example on converting quaternions to euler angles
	# source:
	# http://www.theconstructsim.com/ros-qa-how-to-convert-quaternions-to-euler-angles/
	orientation_q = msg.pose.pose.orientation
	orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
	(roll, pitch, yaw) = euler_from_quaternion (orientation_list)

	# the following block catches the yaw discontinuity and increments the wrap counter
	# valid yaw range is from -pi to pi
	if old_yaw < -threshold and yaw > threshold: # from -pi to pi (increasing negative)
		num_wraps = num_wraps - 1
	elif old_yaw > threshold and yaw < -threshold:
		num_wraps = num_wraps + 1

	# establish the new value of wrapped_yaw using the updated num_wraps
	wrapped_yaw = yaw + 2*math.pi*num_wraps

	# update old_yaw, this variable is used in the wrap catch block
	old_yaw = yaw

	# write the converted angles to the angular properties of the position message
	# also convert the radian positions to degrees
	pos_msg.angular.roll  = roll * 180/math.pi
	pos_msg.angular.pitch = pitch * 180/math.pi
	pos_msg.angular.yaw   = wrapped_yaw * 180/math.pi

	# make sure we publish the message
	pub1.publish(pos_msg)

if __name__== '__main__':
	try:




		# create the node
		rospy.init_node('quat_to_eul')
		# create the publisher
		pub = rospy.Publisher('/eul', Position, queue_size=10)
		#pub1 = rospy.Publisher('/eul1', Position, queue_size=10)
		# create the subscriber, subscribe to the /odom message which is created by
		# the turtlebot gazebo simulation
		sub = rospy.Subscriber ('/tb1/odom', Odometry, get_rotation, (pub))
		#sub = rospy.Subscriber ('/tb1/odom', Odometry, get_rotation1, (pub))
		# create a rate object for controlling the refresh rate, argument is the
		# desired refresh rate in Hz
		r = rospy.Rate(100) #Hz

		while not rospy.is_shutdown():

			# use the sleep function of the rate object to sleep the proper
			# duration according to the rate set using the Rate() function

			if coin == 0:
				clear()
				print msg0
			if coin == 50:
				clear()
				print msg1
			if coin == 100:
				clear()
				print msg2
			if coin == 150:
				clear()
				print msg3
			if coin == 200:
				clear()
				print msg4

			coin = coin + 1
			if coin >250:
				coin =0


			r.sleep()

	except rospy.ROSInterruptException:
		pass
