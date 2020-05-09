import QRCode as myqr
import ImageProcess as imgp
import cv2
from PIL import Image

if __name__ == '__main__':
    mq = myqr.QRCode()

    src_img = cv2.imread(myqr.QRCode.qrfile)
    imgpro = imgp.ImageProcess()
    imgpro.src_image = src_img
    imgpro.image_process(imgpro.src_image)
    
    # cv2.imshow('1',imgpro.dst_image)
    # cv2.waitKey()

    # cv2图转为Image图
    Img_dst_image = Image.fromarray(cv2.cvtColor(imgpro.qrcode,cv2.COLOR_BGR2RGB))

    data = mq.decode_qrcode_zxbar(Img_dst_image)




