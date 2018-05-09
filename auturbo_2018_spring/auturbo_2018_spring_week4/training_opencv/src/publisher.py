#!/usr/bin/env python
import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage


class Publisher():
    def __init__(self):
        self.selecting_sub_image = "raw"

        if self.selecting_sub_image == "compressed":
            self._sub = rospy.Subscriber('/usb_cam/image_raw/compressed', CompressedImage, self.callback, queue_size=1)
        else:
            self._sub = rospy.Subscriber('/usb_cam/image_raw', Image, self.callback, queue_size=1)

        self._pub1 = rospy.Publisher('/image_compressed', CompressedImage, queue_size=1)
        self._pub2 = rospy.Publisher('/image_raw', Image, queue_size=1)

        self.bridge = CvBridge()

    def callback(self, image_msg):

        if self.selecting_sub_image == "compressed":
            #converting compressed image to opencv image
            np_arr = np.fromstring(image_msg.data, np.uint8)
            cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        elif self.selecting_sub_image == "raw":
            cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        cv2.imshow('cv_image', cv_image), cv2.waitKey(1)

        #publising compressed image
        msg_raw_image = CompressedImage()
        msg_raw_image.header.stamp = rospy.Time.now()
        msg_raw_image.format = "jpeg"
        msg_raw_image.data = np.array(cv2.imencode('.jpg', cv_image)[1]).tostring()
        self._pub1.publish(msg_raw_image)

        #publishing raw image
        self._pub2.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))

    def main(self):
        rospy.spin()

if __name__ == '__main__':
    rospy.init_node('publisher')
    node = Publisher()
    node.main()