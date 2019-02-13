# ME401-Intoduction-to-R.O.S

This Branch contains homework 3

# ME 401/5501–Robotics and Unmanned Systems HW_3  
### DUE February 12th

For this assignment you will be using ROS and Gazebo to simulate the Turtlebot3 Burger platform.  Help in loading the simulation can be found at http://emanual.robotis.com/docs/en/platform/turtlebot3/simulation/. Make sure to go to the Gazebo part of the E-manual. When setting the model type, replace “${TB3_MODEL}” with “burger.”

### Problem 1:

Create a ROS node that follows the given set of prescribed waypoints: [0,0], [0,1], [2,2], [3, -3]. Start your robot at [0,0]. Create a plot of the X, Y coordinates to show how well your robot follows the desired path. Use a maximum translational speed of 0.2m/s (the slower the easier to debug).

Submit your Python code.

### Problem 2:

Modify your heading feedback controller software to incorporate a minimum turning radius (simulating a traditional car style robot). This is accomplished by limiting the angular velocity command based upon the translational velocity command. Use a minimum radius of 0.5meters for this assignment.

Create a plot of the X, Y coordinates to show how well the robot follows the same prescribed waypoints. 

Submit your Python code.


