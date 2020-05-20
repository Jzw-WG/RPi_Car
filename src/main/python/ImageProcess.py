import os
import sys
import time
import logging
import random
from PIL import Image
import numpy as np
import cv2
import math
import numpy
from enum import Enum
import QRCode as myqr

logger = logging.getLogger(__name__)    #记录数据

if not logger.handlers:
    logging.basicConfig(level = logging.INFO)

DEBUG = (logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')   #记录调式过程

class ImageProcess:
    def __init__(self):
        """initializes all values to presets or None if need to be set
        """
        self.src_image = None        
        self.gray_src_image = None
        self.threshold_image = None
        self.blur_image = None
        self.dst_image = None
        self.qrcode = None

        self.old_src_image = self.src_image
        self.old_gray_src_image = self.gray_src_image
        self.old_dst_image = self.dst_image
        self.point_image = None

        self.optical_flow_image = None
        """cv_threshold params
        """
        self.cv_threshold_thresh = 220.0
        self.cv_threshold_maxval = 255.0
        self.cv_threshold_type = cv2.THRESH_BINARY

        """opticalflow params
        """
        
        # ShiTomasi 角点检测参数
        self.feature_params = dict( maxCorners = 100,
                            qualityLevel = 0.1,
                            minDistance = 7,
                            blockSize = 7 )

        # lucas kanade光流法参数
        self.lk_params = dict( winSize  = (15,15),
                        maxLevel = 2,
                        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # 创建随机颜色
        self.color = np.random.randint(0,255,(100,3))
        self.p0 = None

        """blur params
        """
        self.blur_type = BlurType.Median_Filter
        self.blur_radius = 1.8018018018018018

    def image_process(self, input):
        self.src_image = input
        self.gray_src_image = self.desaturate(self.src_image)
        self.threshold_image = self.cv_threshold(self.gray_src_image,self.cv_threshold_thresh,self.cv_threshold_maxval,self.cv_threshold_type)
        self.blur_image = self.blur(self.threshold_image, self.blur_type, self.blur_radius)

        self.dst_image = self.blur_image

        self.qrcode = self.dst_image
        # self.get_qrcode_from_image()

    def get_qrcode_from_image(self):
        #读取图片，灰度化
        #腐蚀、膨胀
        kernel = np.ones((5,5),np.uint8)
        erode_Img = cv2.erode(self.dst_image,kernel)
        eroDil = cv2.dilate(erode_Img,kernel)
        # cv2.imshow("rotateImg",eroDil)
        # cv2.waitKey()
        #边缘检测
        canny = cv2.Canny(eroDil,50,150)
        # cv2.imshow("rotateImg",canny)
        # cv2.waitKey()
        #霍夫变换得到线条
        lines = cv2.HoughLinesP(canny, 0.8, np.pi / 180, 90,minLineLength=100,maxLineGap=10)
        drawing = np.zeros(self.dst_image.shape[:], dtype=np.uint8)
        #画出线条
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(drawing, (x1, y1), (x2, y2), (0, 255, 0), 1, lineType=cv2.LINE_AA)
        
        # cv2.imshow("rotateImg",drawing)
        # cv2.waitKey()
        """
        计算角度,因为x轴向右，y轴向下，所有计算的斜率是常规下斜率的相反数，我们就用这个斜率（旋转角度）进行旋转
        """
        k = float(y1-y2)/(x1-x2)
        thera = np.degrees(math.atan(k))

        """
        旋转角度大于0，则逆时针旋转，否则顺时针旋转
        """
        rotateImg = self.rotate(self.dst_image,thera)
        self.qrcode = rotateImg 
        # cv2.imshow("rotateImg",rotateImg)
        # cv2.waitKey()

    def optical_flow(self):

        old_gray = ImageProcess.desaturate(self.old_src_image)

        # 创建一个蒙版用来画轨迹
        mask = np.zeros_like(self.old_src_image)

        frame_gray = ImageProcess.desaturate(self.src_image) #灰度化

        # 计算光流
        p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, self.p0, None, **self.lk_params)
        # 选取好的跟踪点
        good_new = p1[st==1]
        good_old = self.p0[st==1]

        # 画出轨迹
        for i,(new,old) in enumerate(zip(good_new,good_old)):
            a,b = new.ravel()#多维数据转一维,将坐标转换后赋值给a，b
            c,d = old.ravel()
            mask = cv2.line(mask, (a,b),(c,d), self.color[i].tolist(), 2)#画直线
            self.point_image = cv2.circle(self.src_image,(a,b),5, self.color[i].tolist(), -1)#画点
        self.optical_flow_image = cv2.add(self.point_image,mask) # 将画出的线条进行图像叠加

        # 更新上一帧的图像和追踪点
        self.p0 = good_new.reshape(-1,1,2)

    @staticmethod
    def rotate(image,angle,center=None,scale=1.0):
        (w,h) = image.shape[:]
        if center is None:
            center = (w//2,h//2)   
        wrapMat = cv2.getRotationMatrix2D(center,angle,scale)    
        return cv2.warpAffine(image,wrapMat,(h,w))
    
    @staticmethod
    def cv_threshold(src, thresh, max_val, type):
        return cv2.threshold(src, thresh, max_val, type)[1]
    
    @staticmethod
    def desaturate(src):
        try:
            (a, b, channels) = src.shape
            if(channels == 1):
                return numpy.copy(src)
            elif(channels == 3):
                return cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
            elif(channels == 4):
                return cv2.cvtColor(src, cv2.COLOR_BGRA2GRAY)
            else:
                raise Exception("Input to desaturate must have 1, 3 or 4 channels")
        except:
            return numpy.copy(src)

    @staticmethod
    def blur(src, type, radius):
        if(type is BlurType.Box_Blur):
            ksize = int(2 * round(radius) + 1)
            return cv2.blur(src, (ksize, ksize))
        elif(type is BlurType.Gaussian_Blur):
            ksize = int(6 * round(radius) + 1)
            return cv2.GaussianBlur(src, (ksize, ksize), round(radius))
        elif(type is BlurType.Median_Filter):
            ksize = int(2 * round(radius) + 1)
            return cv2.medianBlur(src, ksize)
        else:
            return cv2.bilateralFilter(src, -1, round(radius), round(radius))

BlurType = Enum('BlurType', 'Box_Blur Gaussian_Blur Median_Filter Bilateral_Filter')

if __name__ == '__main__':
    img_process = ImageProcess()
    filename = myqr.QRCode.qr_image_path + myqr.QRCode.qr_file_name
    img_process.src_image = cv2.imread(filename)
    # img_process.get_qrcode_from_image()
    img_process.gray_src_image = img_process.desaturate(img_process.src_image)
    img_process.dst_image = img_process.cv_threshold(img_process.gray_src_image,220,255,cv2.THRESH_BINARY)
    cv2.imshow('1',img_process.dst_image)
    cv2.waitKey()

