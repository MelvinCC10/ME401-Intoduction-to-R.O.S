#!/usr/bin/env python

# Author:
# Data:
# Purpose:

import rospy, time, csv, os, datetime
from beginner_tutorials.msg import Position
from nav_msgs.msg import Odometry

def callback_pos(data, data_out):
	data_out.linear.x = data.pose.pose.position.x
	data_out.linear.y = data.pose.pose.position.y
	data_out.linear.z = data.pose.pose.position.z

def callback_ori(data, data_out):
	data_out.angular.roll  = data.angular.roll
	data_out.angular.pitch = data.angular.pitch
	data_out.angular.yaw   = data.angular.yaw

def callback_cmd(data, data_out):
	data_out.linear.x = data.pose.pose.position.x
	data_out.linear.y = data.pose.pose.position.y
	data_out.linear.z = data.pose.pose.position.z
    data_out.angular.roll  = data.angular.roll
	data_out.angular.pitch = data.angular.pitch
	data_out.angular.yaw   = data.angular.yaw




if __name__ == "__main__":

	try:

		# create a node
		rospy.init_node('LogFileNode', anonymous=True)

        position = Position()
		rospy.Subscriber('/eul', Position, callback_ori, (position))
		rospy.Subscriber('/odom', Odometry, callback_pos, (position))
        rospy.Subscriber('cmd_vel', Twist, callback_cmd, (cmd))

		# create a rate object for timing, the argument is in Hz
		r = rospy.Rate(100) #HZ

		# this will constitute the header for the columns in the csv file, this is simply because
		# it is the first line which will be written
		myData = ["x,y,z,roll,pitch,yaw,cmd.x,cmd.yaw"]

		# the following code creates a base filename containing the data and time
		fileNameBase = "./scripts/log_files/" + datetime.datetime.now().strftime("%b_%d_%H_%M")

		# the end of the file will always be ".csv"
		fileNameSuffix = ".csv"

		# this number will only be used if the filename already exists
		num = 1

		# compose the complete filename from the component parts, don't use num yet
		fileName = fileNameBase + fileNameSuffix

		# while loop will execute until we have a unique filename
		while os.path.isfile(fileName):
			# if the filename is not unique, add a number to the end of it
			fileName = fileNameBase + "_" + str(num) + fileNameSuffix
			# increments the number in case the filename is still not unique
			num = num + 1

		# now that we have a good filename open it, the "a" option is "append", the default
		# behavior is to overwrite the file each time the file is opened, in this case we
		# want to keep the existing file but add a new line each time we open so we use
		# the append option
		myFile = open(fileName, 'a')
		# using the newly create file object
		with myFile:
			# create a csv writer object which is attached to the file object
			writer = csv.writer(myFile)
			# write a single row, there are other write functions which can be used,
			# since this one only writes a single row it automatically adds a newline
			# to the end of the data
			writer.writerow(myData)

		while not rospy.is_shutdown():

			# this represents the "real" data which we want to write to the file
			myData = [linear.x,linear.y,linear.z,angular.roll,angular.pitch,angular.yaw]

			# print status message
			print "write to file"

			# same as the code block above
			myFile = open(fileName, 'a')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerow(myData)

			# print status message
			print "write complete, waiting"

			r.sleep()

	except rospy.ROSInterruptException:

		pass
