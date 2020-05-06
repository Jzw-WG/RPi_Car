import sys
import os
o_path = os.getcwd()
sys.path.append(o_path)
import src.main.python.QRCode as myqr

myqr.QRCode.generate_qrcode(os.getcwd() + '/src/main/image/' + 'qr.png', 'w')