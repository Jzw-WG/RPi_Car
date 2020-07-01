#!/usr/bin/python
#-- coding:utf8 --
import RPi.GPIO as GPIO
import serial
import time
class CarControl:
    MAX_LEFT_RIGHT_ANGLE = 45
    DEFAULT_RECT_HEIGHT_RATE = 0.3
    CENTER_RANGE = 0.05
    # CHANNEL_LIST = [17, 27, 22, 18, 23, 24, 25, 12]
    def __init__(self):
        self.ser = None

    @staticmethod
    def get_left_right_command(rect_center, image_width):
        if rect_center < image_width/2 - image_width*CarControl.CENTER_RANGE:
            command = 'left'
            angle = CarControl.MAX_LEFT_RIGHT_ANGLE * (image_width/2 - rect_center) / (image_width/2)
        elif rect_center > image_width/2 + image_width*CarControl.CENTER_RANGE:
            command = 'right'
            angle = CarControl.MAX_LEFT_RIGHT_ANGLE * (rect_center - image_width/2) / (image_width/2)
        elif rect_center >= image_width/2 - image_width*CarControl.CENTER_RANGE and rect_center <= image_width/2 + image_width*CarControl.CENTER_RANGE:
            command = 'no'
            angle = 0
        else:
            command = 'no'
            angle = 0
        param = angle
        return command,param

    @staticmethod
    def get_forward_backward_command(rect_height, image_height):
        if rect_height/image_height < CarControl.DEFAULT_RECT_HEIGHT_RATE:
            command = 'forward'
            distance = -1
        elif rect_height/image_height > CarControl.DEFAULT_RECT_HEIGHT_RATE:
            command = 'backward'
            distance = -1
        else:
            command = 'stop'
            distance = 0
        param = distance
        return command,param

    def initial(self):
        # GPIO.setup(CHANNEL_LIST, GPIO.OUT)
        self.ser = serial.Serial('/dev/ttyAMA0', 115200)

    def transfer_rect_to_control(self, rect, image_shape):
        self.initial()
        if rect != None and image_shape != None:
            rect_left = rect.left
            rect_center = rect.left + rect.width/2
            rect_height = rect.height
            image_width = image_shape[1]
            image_height = image_shape[0]
            command1,param1 = self.get_left_right_command(rect_center, image_width)
            command2,param2 = self.get_forward_backward_command(rect_height, image_height)
            self.transfer_command_to_control(command1,param1,command2,param2)
    
    def transfer_command_to_control(self,command1,param1,command2,param2):
        if command1 == 'left':           
            if command2 == 'forward':
                self.forward_left(param1, param2)
            elif command2 == 'backward':
                self.backward_left(param1, param2)
            else:
                self.turn_left(param1)
        elif command1 == 'right':           
            if command2 == 'forward':
                self.forward_right(param1, param2)
            elif command2 == 'backward':
                self.backward_right(param1, param2)
            else:
                self.turn_right(param1)
        else:
            if command2 == 'forward':
                self.go_forward(param2)
            elif command2 == 'backward':
                self.go_backward(param2)
            else:
                self.stop()

    # def changeGPIO(command, angle, distance):
    #     bits = bin(angle)
    #     if command == 'stop':
    #         # GPIO 17 and 27 output 11 = stop
    #         GPIO.output(CHANNEL_LIST[0], GPIO.HIGH)
    #         GPIO.output(CHANNEL_LIST[1], GPIO.HIGH)
    #     if command == 'left':
    #        # GPIO 17 and 27 output 01 = left
    #         GPIO.output(CHANNEL_LIST[0], GPIO.LOW)
    #         GPIO.output(CHANNEL_LIST[1], GPIO.HIGH)
    #         # GPIO 18,23,24,25,12 output = bin(angle)
    #         GPIO.output(CHANNEL_LIST[4], int(bits[-5]))
    #         GPIO.output(CHANNEL_LIST[5], int(bits[-4]))
    #         GPIO.output(CHANNEL_LIST[6], int(bits[-3]))
    #         GPIO.output(CHANNEL_LIST[7], int(bits[-2]))
    #         GPIO.output(CHANNEL_LIST[8], int(bits[-1]))
    #     elif command == 'right':
    #         # GPIO 17 and 27 output 10 = right
    #         GPIO.output(CHANNEL_LIST[0], GPIO.HIGH)
    #         GPIO.output(CHANNEL_LIST[1], GPIO.LOW)
    #         # GPIO 18,23,24,25,12 output = bin(angle)
    #         GPIO.output(CHANNEL_LIST[4], int(bits[-5]))
    #         GPIO.output(CHANNEL_LIST[5], int(bits[-4]))
    #         GPIO.output(CHANNEL_LIST[6], int(bits[-3]))
    #         GPIO.output(CHANNEL_LIST[7], int(bits[-2]))
    #         GPIO.output(CHANNEL_LIST[8], int(bits[-1]))
    #     if command == 'forward':
    #         # GPIO 22 output 0 = forward
    #         GPIO.output(CHANNEL_LIST[2], GPIO.LOW)
    #     elif command == 'backward':
    #         # GPIO 22 output 1 = backward
    #         GPIO.output(CHANNEL_LIST[2], GPIO.HIGH)
    
    # 1:left 2:right 3:forward 4:backward 5:forward_left 6:forward_right 7:backward_left 8:backward_right
    def changeTDXRDX(self, command, angle, distance):
        if self.ser != None:
            self.ser.write(command+str(int(angle)).encode('utf-8'))

    def turn_left(self, angle):
        self.changeTDXRDX('1', angle, '')
        print('turn left' + ', angle：',angle)

    def turn_right(self, angle):
        self.changeTDXRDX('2', angle, '')
        print('turn right' + ', angle：',angle)

    def go_forward(self, distance):
        self.changeTDXRDX('3', '', distance)
        print('go forward' + ', distance：',distance)
  
    def go_backward(self, distance):
        self.changeTDXRDX('4', '', distance)
        print('go backward' + ', distance：',distance)
    
    def forward_left(self, angle, distance):
        self.changeTDXRDX('5', angle, distance)
        print('forward_left' + ', angle：',angle, ', distance：',distance)

    def forward_right(self, angle, distance):
        self.changeTDXRDX('6', angle, distance)
        print('forward_right' + ', angle：',angle, ', distance：',distance)

    def backward_left(self, angle, distance):
        self.changeTDXRDX('7', angle, distance)
        print('backward_left' + ', angle：',angle, ', distance：',distance)
  
    def backward_right(self, angle, distance):
        self.changeTDXRDX('8', angle, distance)
        print('backward_right' + ', angle：',angle, ', distance：',distance)

    def stop(self):
        self.changeTDXRDX('stop', '', '')
        print('stop')
    
