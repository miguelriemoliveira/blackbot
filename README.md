# Blackbot
**ROS** utils for the blackbot robotic system

## Table of Contents

* [The Robot](#therobot)
* [Installation](#installation)
* [Usage](#usage)
* [Hand in eye calibration](#handineyecalibration)
* [Kinect2 calibration](#kinect2calibration)
* [Calibration Setup](#calibrationsetup)
* [Credits](#credits)

## <a name="therobot"></a>The Robot

The system is composed of an  [kinect2 camera](https://en.wikipedia.org/wiki/Kinect_for_Xbox_One) mounted on top of a [flir pand and tilt unit](http://www.flir.com/mcs/view/?id=63554).

![Image of blackbot](https://github.com/miguelriemoliveira/blackbot/blob/master/docs/blackbot.jpg)

## <a name="installation"></a>Installation

TODO ...

## <a name="usage"></a> Usage

To launch the complete robot system, i.e., camera drivers, pan and tilt drivers and robot_state_publisher run

```shell
roslaunch blackbot_bringup all.launch calibrated:=true
```

You can ommit the calibrated:=true (its the default). To visualize the system, run

```shell
roslaunch blackbot_bringup visualize.launch
```

## <a name="handineyecalibration"></a>Hand in eye calibration

A calibration procedure estimates a transformation from the end link of the pan and tilt to the first link of the camera. In this case, a transformation from the **tilt_assembly** link to the **camera_link** link. Check the [Calibration Setup](#calibrationsetup) section to learn more about how the system should be setup for calibration.

The [kinect2 calibration](https://github.com/code-iai/iai_kinect2/tree/master/kinect2_calibration) should be completed beforehand.

To calibrate (With the setup already mounted), first launch the system in **uncalibrated mode**

```shell
roslaunch blackbot_bringup all.launch calibrated:=false manual_command:=true
```

Then, startup a visualization in rviz

```shell
roslaunch blackbot_calibration visualize.launch
```

Finally, run the calibration

```shell
roslaunch blackbot_calibration calibration.launch marker_id:=582 marker_size:=0.144 interactive:=false 
```

To achieve a very accurate calibration, the procedure should be executed in interactive mode (interactive:=true), meaning that the user should confirm mannually each sample to be used in the calibration procedure.

You should see something like this

![Calibration desktop](https://github.com/miguelriemoliveira/blackbot/blob/master/docs/calibration_desktop.png)

Then move the pan and tilt manually so that several views of the aruco marker are captured. As more views are collected, the estimated transformation should become more accurate, so the camera reference frames should approach the expected pose in rviz.

After collecting enough views and when you're satisfied with the transformation (either the numbers which are displayed or the reference frames which are shown in rviz), you may store the calibration by running

```shell
rosrun blackbot_calibration store_calibration.py
```

After that the estimated calibration is stored in **(...)/blackbot_calibration/calibration/hand_in_eye.urdf.xacro** . To use this new calibration just kill everything and re execute the drivers in **calibrated more**

```shell
roslaunch blackbot_bringup bringup.launch calibrated:=true
```

in fact you can skip the **calibrated:=true** part since its the default value for the launch file argument.

Here is an example of a calibrated system.

<p align="center">
<img src="https://github.com/miguelriemoliveira/blackbot/blob/master/docs/calibrated_system.png" width="850">
</p>

## <a name="kinect2calibration"></a>Kinect2 calibration

## <a name="calibrationsetup"></a>Calibration Setup

Prior to the calibration, there will be no connection between the pan and tilt and the camera, and so the tf tree obtained with

```bash
rosrun tf view_frames && evince frames.pdf
```

should be something like this:

![frames_before_calibration](https://github.com/miguelriemoliveira/blackbot/blob/master/docs/tf_uncalibrated.png)

and after calibration, the tf tree should look like this:

<p align="center">
<img src="https://github.com/miguelriemoliveira/blackbot/blob/master/docs/tf_calibrated.png" width="650">
</p>

The calibration procedure is based on the [https://github.com/jhu-lcsr/aruco_hand_eye](https://github.com/jhu-lcsr/aruco_hand_eye) ros package. During the calibration the camera should view an aruco marker so that the **camera to aruco transform** is accurately estimated. An aruco marker pdf for printing can be generated at [http://terpconnect.umd.edu/~jwelsh12/enes100/markergen.html](http://terpconnect.umd.edu/~jwelsh12/enes100/markergen.html)

<p align="center">
<img src="https://github.com/miguelriemoliveira/blackbot/blob/master/docs/aruco_marker585.png" width="350">
</p>

In this image and throughout this tutorial, we assume a marker id 582 with size 0.144

Note that, in order to achieve the accurate calibration results, the rgb camera of the asus must be calibrated prior to this procedure, using a chessboard and a monocular rgb calibration

```shell
rosrun camera_calibration cameracalibrator.py image:=/camera/rgb/image_raw camera:=/camera/rgb --size 7x5 --square 0.03
```
For detailed tutorials on that see [http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration](http://wiki.ros.org/camera_calibration/Tutorials/MonocularCalibration) and [http://wiki.ros.org/openni_launch/Tutorials/IntrinsicCalibration](http://wiki.ros.org/openni_launch/Tutorials/IntrinsicCalibration)



## <a name="license"></a>License

I am using a kinect2 model from [https://github.com/code-iai/iai_robots/tree/master/iai_kinect2_description](https://github.com/code-iai/iai_robots/tree/master/iai_kinect2_description)

The kinect2 meshes are Copyright Universitaet Bremen - Institute for Artificial Intelligence (Prof. Michael Beetz).
Author: Alexis Maldonado Released under the CC BY-SA 4.0 license. https://creativecommons.org/licenses/by-sa/4.0/
