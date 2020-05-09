import qrcode
import os
import sys
import time
import zxing
from pyzbar import pyzbar
import logging
import random
import numpy
from PIL import Image

logger = logging.getLogger(__name__)    #记录数据

if not logger.handlers:
    logging.basicConfig(level = logging.INFO)

DEBUG = (logging.getLevelName(logger.getEffectiveLevel()) == 'DEBUG')   #记录调式过程

class QRCode:
    qr_image_path = os.getcwd() + '/src/main/image/'   #存储位置
    qr_file_name = 'testqr2.png' 
    qrfile = qr_image_path + qr_file_name                                  

    @staticmethod
    def generate_qrcode(qrimagename, inputdata=''):
        qr = qrcode.QRCode(     
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )   #设置图片格式
        
        # data = input()  #运行时输入数据
        data = inputdata
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image()
        img.save(qrimagename)  #生成图片

        # 打开生成的二维码 
        if sys.platform.find('darwin') >= 0:
            os.system('open %s' % qrimagename)        
        elif sys.platform.find('linux') >= 0:
            os.system('xdg-open %s' % qrimagename)
        else:
            os.system('call %s' % qrimagename)
        # time.sleep(5)   #间隔5个单位
        # os.remove(QRImagePath)  #删除图片

    # 在当前目录生成临时文件，规避java的路径问题
    @staticmethod
    def decode_qrcode_zxing(image, filename=''):
        if filename !='':
            img = Image.open(filename)
        elif image != None:
            img = image
        else:
            logger.error(u'无二维码')
            
        ran = int(random.random() * 100000)     #设置随机数据的大小
        img.save('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
        zx = zxing.BarCodeReader()      #调用zxing二维码读取包
        data = ''
        zxdata = zx.decode('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))    #图片解码

        # 删除临时文件
        os.remove('%s%s.jpg' % (os.path.basename(filename).split('.')[0], ran))
            
        if zxdata:
            logger.debug(u'zxing识别二维码:%s,内容: %s' % (filename, zxdata))
            data = zxdata
        else:
            logger.error(u'识别zxing二维码出错:%s' % (filename))
            img.save('%s-zxing.jpg' % filename)
        return data     #返回记录的内容
    
    @staticmethod
    def decode_qrcode_zxbar(image, filename=''):
        if filename !='':
            if os.path.isfile(filename):
                # 从本地加载二维码图片
                img = Image.open(filename)
            else:
                # 从网络下载并加载二维码图片
                rq_img = requests.get(filename).content
                img = Image.open(BytesIO(rq_img))
        elif image != None:
            img = image
        else:
            logger.error(u'无二维码')        
    
        # img.show()  # 显示图片，测试用
    
        txt_list = pyzbar.decode(img)
    
        for txt in txt_list:
            barcodeData = txt.data.decode("utf-8")
        return barcodeData


if __name__ == '__main__':
    filename = QRCode.qr_image_path + QRCode.qr_file_name
    # zxing二维码识别
    # ltext = QRCode.decode_qrcode_zxing(None, filename)  #将图片文件里的信息转码放到ltext里面
    ltext = QRCode.decode_qrcode_zxbar(None, filename)  #将图片文件里的信息转码放到ltext里面
    logger.info(u'[%s]Zxing二维码识别:[%s]!!!' % (filename, ltext))  #记录文本信息            
    print(ltext)    #打印出二维码名字




        
