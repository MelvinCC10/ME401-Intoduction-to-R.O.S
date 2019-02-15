#!/usr/bin/env python
import rospy, time, os, datetime
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry

# callback function for 3DOF linear position
def callback_pos(data, data_out):
	data_out.linear.x = data.pose.pose.position.x
	data_out.linear.y = data.pose.pose.position.y
	data_out.linear.z = data.pose.pose.position.z

# callback function for 3DOF rotation position
def callback_ori(data, data_out):
	data_out.angular.roll  = data.angular.roll
	data_out.angular.pitch = data.angular.pitch
	data_out.angular.yaw   = data.angular.yaw

if __name__ == '__main__':
	try:

		time.sleep(1)

		position = Position()
		rospy.Subscriber('/eul', Position, callback_ori, (position))
		rospy.Subscriber('/odom', Odometry, callback_pos, (position))

		# create a node, the name is arbitrary
		rospy.init_node('PositionNode', anonymous=True)

		rate = rospy.Rate(100) # 100Hz update rate

		time.sleep(1) # pause for 1 second

		while not rospy.is_shutdown():

			# NOTE "\t" in a string inserts a tab character to make the output look nicer
			print "Position"
			print "x: %.2f" % position.linear.x + "\ty:\t%.2f" % position.linear.y + "\tz:\t%.2f" % position.linear.z
			print "Orientation"
			print "roll: %.2f" % position.angular.roll + "\tpitch: %.2f" % position.angular.pitch + "\tyaw: %.2f" % position.angular.yaw

		rate.sleep()

	except rospy.ROSInterruptException:

		pass
