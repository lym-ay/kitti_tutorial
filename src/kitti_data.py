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


    path=rospy.get_param('/kitti_cam/path')
    num=rospy.get_param('/kitti_cam/number')
    rate=rospy.get_param('/kitti_cam/rate')
    rospy.loginfo("path is %s",path)
    rospy.loginfo("number is %d",num)
    rospy.loginfo("rate is %d",rate)
    
    rate=rospy.Rate(rate)

    while not rospy.is_shutdown():
        img=cv2.imread(os.path.join(path,'data_rect/%010d.png'%frame))
        cam_pub.publish(bridge.cv2_to_imgmsg(img,"bgr8"))
        rospy.loginfo("camera image published")
        rate.sleep()
        frame += 1
        frame %=num

