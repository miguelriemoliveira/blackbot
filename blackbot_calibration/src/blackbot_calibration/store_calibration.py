#!/usr/bin/env python
"""

This script will write a new file /blackbot_calibration/calibration/hand_in_eye.urdf.xacro with data collected from the ros system running immediately after the calibration.
It calls rosparams to find out the propper reference frames, and finds the transformation estimated through calibration using a tf listener. Then it will write the a xacro file similar to this
-----------------------------------
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">
<!--This xacro contains six xacro propperties representing a transformation obtained through calibration-->
<!--Calibration generated at 01:28:16, 12/06/2016 -->
<!--This file was written automatically using the "rosrun blackbot_calibration store_calibration.py" command. -->
<xacro:property name="roll" value="0.0217361470355"/>
<xacro:property name="pitch" value="0.061872023059"/>
<xacro:property name="yaw" value="-0.0285727638957"/>
<xacro:property name="x" value="-0.0188701273242"/>
<xacro:property name="y" value="0.0954976920077"/>
<xacro:property name="z" value="0.0916589979185"/>
</robot>
-----------------------------------
"""

#########################
##    IMPORT MODULES   ##
#########################
import rospy
import roslib
import math
import tf
import rospkg
import time

#########################
##      HEADER         ##
#########################
__author__ = "Miguel Riem de Oliveira"
__date__ = "June 2016"
__copyright__ = "Copyright 2016, blackbot"
__credits__ = ["Miguel Riem de Oliveira"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Miguel Oliveira"
__email__ = "m.riem.oliveira@gmail.com"
__status__ = "Development"


#########################
## FUNCTION DEFINITION ##
#########################

##########
## MAIN ##
##########

if __name__ == "__main__":

    #--------------------#
    ### Initialization ###
    #--------------------#

    rospy.init_node('store_calibration')
    rospack = rospkg.RosPack()
    listener = tf.TransformListener()
    rospy.sleep(0.1)

    ### Get the reference frames for the estimated transformation ###
    print("Getting parameter /aruco_tracker/reference_frame")
    tracker_reference_frame = rospy.get_param("/aruco_tracker/reference_frame")

    print("Getting parameter /hand_eye_connector/camera_parent_frame")
    camera_parent_frame = rospy.get_param("/hand_eye_connector/camera_parent_frame")

    ### Get the transformation estimated from calibration ###
    t = rospy.Time()
    print("Waiting for transform from " + tracker_reference_frame + " to " + camera_parent_frame + "\n Will wait a maximum 10 seconds. Note that if you are using the calibration with interactive=true, you add a new calibration instance by pressing enter twice. Only then a transform with the calibration is published.")
    listener.waitForTransform(camera_parent_frame, tracker_reference_frame, t, rospy.Duration(5.0))
    try:
        (trans,rot) = listener.lookupTransform(camera_parent_frame, tracker_reference_frame, t)
    except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
        print("Could not get transform, cannot save calibration.")
        exit()

    print("Collected the transform, will write the xacro.")
    ### store in local variables (and convert quaternion to rpy) ###
    eul = tf.transformations.euler_from_quaternion(rot, axes='sxyz')
    roll = eul[0]
    pitch = eul[1]
    yaw = eul[2]
    x = trans[0]
    y = trans[1]
    z = trans[2]


    ### write to a xml ###
    filename = rospack.get_path('blackbot_calibration') + "/calibration/hand_in_eye.urdf.xacro"
    fo = open(filename, "wb")

    fo.write('<?xml version="1.0"?>\n')
    fo.write('<robot xmlns:xacro="http://www.ros.org/wiki/xacro">\n')
    fo.write('<!--This xacro contains six xacro propperties representing a transformation obtained through calibration-->\n')
    t = (time.strftime("%H:%M:%S, %d/%m/%Y"))
    fo.write('<!--Calibration generated at ' + t +' -->\n' )
    fo.write('<!--This file was written automatically using the "rosrun blackbot_calibration store_calibration" command. -->\n' )
    fo.write('<xacro:property name="roll" value="' + str(roll) + '"/>\n' )
    fo.write('<xacro:property name="pitch" value="' + str(pitch) + '"/>\n' )
    fo.write('<xacro:property name="yaw" value="' + str(yaw) + '"/>\n' )
    fo.write('<xacro:property name="x" value="' + str(x) + '"/>\n' )
    fo.write('<xacro:property name="y" value="' + str(y) + '"/>\n' )
    fo.write('<xacro:property name="z" value="' + str(z) + '"/>\n' )
    fo.write('</robot>\n' )
     
    # Close opend file
    fo.close()


    print('Estimated calibration is stored. You may run the calibrated system with\nroslaunch blackbot_bringup bringup.launch calibrated:=true\n')


