#!/usr/bin/python
#-- coding:utf8 --

# import RPi.GPIO as GPIO
# import serial
# import time


class CarControl:
    MAX_LEFT_RIGHT_ANGLE = 45
    DEFAULT_RECT_HEIGHT_RATE = 0.3
    CENTER_RANGE = 0.05

    # CHANNEL_LIST = [17, 27, 22, 18, 23, 24, 25, 12]
    # def __init__(self):
        # self.ser = None

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

    # def initial():
        # GPIO.setup(CHANNEL_LIST, GPIO.OUT)
        # ser = serial.Serial('/dev/ttyAMA0', 115200)

    def transfer_rect_to_control(self, rect, image_shape):
        # initial()
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
            self.turn_left(param1)
            if command2 == 'forward':
                self.go_forward(param2)
            elif command2 == 'backward':
                self.go_backward(param2)
            else:
                self.stop()
        elif command1 == 'right':
            self.turn_right(param1)
            if command2 == 'forward':
                self.go_forward(param2)
            elif command2 == 'backward':
                self.go_backward(param2)
            else:
                self.stop()
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
    
    # def changeTDXRDX(command, angle, distance):
    #     self.ser.write(command.encode('utf-8'))

    @staticmethod
    def turn_left(angle):
        # changeTDXRDX('left', angle, '')
        print('turn left' + ', angle：',angle)

    @staticmethod
    def turn_right(angle):
        # changeTDXRDX('right', angle, '')
        print('turn right' + ', angle：',angle)

    @staticmethod
    def go_forward(distance):
        # changeTDXRDX('forward', '', distance)
        print('go forward' + ', distance：',distance)

    @staticmethod    
    def go_backward(distance):
        # changeTDXRDX('backward', '', distance)
        print('go backward' + ', distance：',distance)
    
    @staticmethod    
    def stop():
        # changeTDXRDX('stop', '', '')
        print('stop')
    
