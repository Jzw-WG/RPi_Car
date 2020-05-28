# -*- coding: utf-8 -*-
import QRCode as myqr
import ImageProcess as imgp
import cv2
import numpy
import os
import CarControl as cc
from PIL import Image

def camera_app():
    my_qr = myqr.QRCode()
    my_imgpro = imgp.ImageProcess()
    my_car = cc.CarControl()
    # capture = cv2.VideoCapture(0)
    capture = cv2.VideoCapture(os.getcwd() + '/src/main/image/test.mp4')
    # 第一帧
    ret,old_frame = capture.read()
    my_imgpro.src_image = old_frame
    my_imgpro.old_src_image = old_frame
    my_imgpro.old_gray_src_image = my_imgpro.desaturate(old_frame)
    my_imgpro.image_process(old_frame)
    my_imgpro.old_dst_image = my_imgpro.dst_image
    #获取图像中的角点，返回到p0中
    my_imgpro.p0 = cv2.goodFeaturesToTrack(my_imgpro.qrcode, mask = None, **my_imgpro.feature_params)
    i = 0
    
    while(1):
        i = i + 1
        ret,frame = capture.read()
        my_imgpro.image_process(frame)

        # 光流
        # imgpro.optical_flow()

        # cv2.imshow('1',imgpro.optical_flow_image)
        # if cv2.waitKey(1) == ord('q'):
        #     break

        # cv2图转为Image图
        Img_dst_image = Image.fromarray(cv2.cvtColor(my_imgpro.qrcode,cv2.COLOR_BGR2RGB))
        # 不处理直接识别二维码
        # Img_dst_image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        data,rect,polygon = my_qr.decode_qrcode_zbar(Img_dst_image)


        # 更新上一帧的图像和追踪点(光流)
        # old_frame = frame.copy()
        print(i,':',data)

        
        if rect != None and polygon != None:
            draw_image = my_qr.bounding_qrcode_zbar(my_imgpro.src_image,rect,polygon)

        my_car.transfer_rect_to_control(rect,frame.shape)

        cv2.imshow('frame',draw_image)
        if cv2.waitKey(1) == ord('q'):
            break    

def image_app():
    my_qr = myqr.QRCode()
    imgpro = imgp.ImageProcess()       
    src_img = cv2.imread(myqr.QRCode.qrfile)
    
    # imgpro.src_image = src_img
    # imgpro.image_process(imgpro.src_image)
    
    # cv2.imshow('1',imgpro.dst_image)
    # cv2.waitKey()

    # cv2图转为Image图
    # Img_dst_image = Image.fromarray(cv2.cvtColor(imgpro.qrcode,cv2.COLOR_BGR2RGB))
    # 不处理直接识别二维码
    Img_dst_image = Image.fromarray(cv2.cvtColor(src_img,cv2.COLOR_BGR2RGB))
    data = my_qr.decode_qrcode_zbar(Img_dst_image)
    print(data)

if __name__ == '__main__':
    camera_app()




