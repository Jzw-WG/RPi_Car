import qrcode
import os
import sys
import time
import zxing
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
    qr_file_name = 'testqr.png'                                   

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
    def ocr_qrcode_zxing(filename):
        img = Image.open(filename)
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

if __name__ == '__main__':
    filename = QRCode.qr_image_path + QRCode.qr_file_name
    # zxing二维码识别
    ltext = QRCode.ocr_qrcode_zxing(filename)  #将图片文件里的信息转码放到ltext里面
    logger.info(u'[%s]Zxing二维码识别:[%s]!!!' % (filename, ltext))  #记录文本信息            
    print(ltext)    #打印出二维码名字




        
