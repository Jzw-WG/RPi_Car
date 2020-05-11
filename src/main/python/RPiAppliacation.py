import QRCode as myqr
import ImageProcess as imgp
import cv2
from PIL import Image

def camera_app():
    mq = myqr.QRCode()
    imgpro = imgp.ImageProcess()
    capture = cv2.VideoCapture(0)
    i = 0
    while(1):
        i = i + 1
        ret,frame = capture.read()
        imgpro.src_image = frame
        imgpro.image_process(imgpro.src_image)
        
        # cv2.imshow('1',imgpro.dst_image)
        # if cv2.waitKey(1) == ord('q'):
        #     break

        # cv2图转为Image图
        # Img_dst_image = Image.fromarray(cv2.cvtColor(imgpro.qrcode,cv2.COLOR_BGR2RGB))
        # 不处理直接识别二维码
        Img_dst_image = Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB))
        data = mq.decode_qrcode_zxbar(Img_dst_image)
        print(i,':',data)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break    

def image_app():
    mq = myqr.QRCode()
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
    data = mq.decode_qrcode_zxbar(Img_dst_image)
    print(data)

if __name__ == '__main__':
    camera_app()




