#! /usr/bin/python
# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import time

class Sensor:
    def __init__(self):
        self.cry = False
        self.start = 0
        self.count = 0
        pass

    # 初始化树莓派接口14
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(14,GPIO.IN)
        pass

    def destory(self):
        GPIO.cleanup()
        pass
    
    # 取的当前状态
    def get(self):
        self.count = self.count + 1
        ret = False

        # 减少误差,读取2000次
        max_num = 2000
        l = []
        for i in range(max_num):

            if (GPIO.input(14) == GPIO.HIGH):

                l.append('ON')

        print ("%s / %s ")%(len(l),max_num)
        # 如果有800次是ON的话,认为是在哭
        if len(l)> (800):
            self.cry = True
            print "Baby maybe crying~"

        # 每5次清空一次
        if self.count > 5:
            print "Clear"
            self.count = 0
            self.cry = False

        return self.cry




