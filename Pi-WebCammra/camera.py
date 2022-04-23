# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
import datetime
import os
from PIL import Image as image
from numpy import *

from flask import flash

class Camera():

    def __init__(self,num):
        self.cap = cv2.VideoCapture(num)
        self.pic_list = None
        self.change_size = True
        self.width = 200
        self.height= 200
        self.default_w = 400
        self.default_h = 400
        self.quality = 50
        pass

    # 拍照
    def take_picture(self,path):
        ret, frame = self.cap.read()

        if self.cap.isOpened():

            frame = cv2.imencode('.jpg', frame)[1].tostring()
            #获得当前时间
            now = datetime.datetime.now()
            #转换为指定的格式:
            otherStyleTime = now.strftime("%Y%m%d_%H%M%S")
            path = path +'/'+otherStyleTime +'.jpg'
            print 'take picture!'
            # 路径不能已/开头
            file_object = open(path[1:], 'w')
            file_object.write(frame)
            file_object.close()
            # 保存文件后的路径


            return path
        else:
            return ('static/img/error.png')

    def gen(self):

        while True:
            ret, frame = self.cap.read()

            in_img = image.fromarray(frame)

            # 由于网速不行,需要对图片进行压缩
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),self.quality]

            if self.change_size == False:
                    self.width = frame.shape[0]
                    self.height = frame.shape[1]

            self.default_w = frame.shape[0]
            self.default_h = frame.shape[1]

            out_img = self.resizeImg(in_img,self.width,self.height)

            frame = cv2.imencode('.jpg', array(out_img),encode_param)[1].tostring()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def  get_all_picture(self):
            root = os.getcwd() + '/static/pic/'
            self.pic_list = []
            pic_path_ab = []

            for x in os.listdir(root):
                self.pic_list.append(root + x)
                pic_path_ab.append(x)

            return pic_path_ab

    # 删除图片
    def del_pic(self,name):
        for item in self.pic_list:
            # 查找还有name的路径
            if item.count(name):
                os.remove(item)
                self.pic_list.remove(item)


    def scale_video(self,num):
        self.change_size = True
        self.height = self.height * num / 100
        self.width = self.width * num /100

    def quality_video(self,num):
        self.quality = self.quality * num /100
        pass

    def reset_video(self):
        self.width = self.default_w
        self.height = self.default_h
        self.quality = 100
        self.change_size = False
        pass

    #等比例压缩图片
    def resizeImg(self,ori_img, dst_w,dst_h):


        im = ori_img
        ori_w,ori_h = im.size
        widthRatio = heightRatio = None
        ratio = 1
        if (ori_w and ori_w > dst_w) or (ori_h and ori_h > dst_h):
            if dst_w and ori_w > dst_w:
                widthRatio = float(dst_w) / ori_w #正确获取小数的方式
            if dst_h and ori_h > dst_h:
                heightRatio = float(dst_h) / ori_h

            if widthRatio and heightRatio:
                if widthRatio < heightRatio:
                    ratio = widthRatio
                else:
                    ratio = heightRatio

            if widthRatio and not heightRatio:
                ratio = widthRatio
            if heightRatio and not widthRatio:
                ratio = heightRatio

            newWidth = int(ori_w * ratio)
            newHeight = int(ori_h * ratio)
        else:
            newWidth = ori_w
            newHeight = ori_h

        return im.resize((newWidth,newHeight),image.ANTIALIAS)

