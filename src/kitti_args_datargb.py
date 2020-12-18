#!/usr/bin/env python
import cv2
import os
import sys
import getopt

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

#DATA_PATH='/home/simul/kitti/2011_09_26/2011_09_26_drive_0005_sync'
#DATA_PATH1='/media/simul/newvol/dataset/KITTI/PerspectiveImages/data_2d_raw/2013_05_28_drive_0000_sync'

if __name__=='__main__':
    frame=0
    rospy.init_node('kitti_node',anonymous=True)
    cam_pub=rospy.Publisher('kitti_cam',Image,queue_size=10)
    bridge=CvBridge()

    rate=rospy.Rate(10)
    try:
        options, args = getopt.getopt(sys.argv[1:],"hp:n:")
    except getopt.GetoptError:
        sys.exit()

    path=''
    num=0
    for option,value in options:
        if option == '-h':
            print("kitti_args -p [image path] -n [number of image]")
            sys.exit()
        if option == '-p':
            path = value
        if option == '-n':
            num = int(value)

    while not rospy.is_shutdown():
        img=cv2.imread(os.path.join(path,'data_rgb/%010d.png'%frame))
        cam_pub.publish(bridge.cv2_to_imgmsg(img,"bgr8"))
        rospy.loginfo("camera image published")
        rate.sleep()
        frame += 1
        frame %=num

