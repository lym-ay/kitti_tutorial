#!/usr/bin/env python
import cv2
import os
import numpy as np

import rospy
from std_msgs.msg import Header
from sensor_msgs.msg import Image,PointCloud2
import sensor_msgs.point_cloud2 as pcl2
from cv_bridge import CvBridge

DATA_PATH1='/home/simul/kitti/2011_09_26/2011_09_26_drive_0005_sync'

if __name__=='__main__':
    frame1=0
    frame2=0
    rospy.init_node('kitti_cloud_node',anonymous=True)
    cam_pub1=rospy.Publisher('kitti_cloud',Image,queue_size=10)
    pcl_pub=rospy.Publisher('kitti_point_cloud',PointCloud2,queue_size=10)
    bridge=CvBridge()

    rate=rospy.Rate(10)
    while not rospy.is_shutdown():
        img1=cv2.imread(os.path.join(DATA_PATH1,'image_00/data/%010d.png'%frame1))
        point_cloud = np.fromfile(os.path.join(DATA_PATH1,'velodyne_points/data/%010d.bin'%frame1),dtype=np.float32).reshape(-1,4)

        cam_pub1.publish(bridge.cv2_to_imgmsg(img1,"bgr8"))
    
        header = Header()
        header.stamp = rospy.Time.now()
        header.frame_id = 'map'
        pcl_pub.publish(pcl2.create_cloud_xyz32(header,point_cloud[:,:3]))
        rospy.loginfo("camera image published")
        rate.sleep()
        frame1 += 1
        frame1 %=124


