# -*- coding: UTF-8 -*-
#!/usr/bin/env python

import cv2
from flask import Flask,render_template,Response,url_for,flash,request,redirect,Markup
import markdown2
import os
import datetime
from camera import Camera


app = Flask(__name__)
app.secret_key = 'Test'
cam = Camera(0)

@app.route('/')
def index():
    return render_template('index.html')

# 拍照取的图片
@app.route('/pic_now')
def current_picture():
    path = cam.take_picture(url_for('static',filename='pic'))
    return render_template('current_picture.html',path=path)
#  拍视频
@app.route('/video_now')
def current_video():
    return render_template('video_push.html')

# 对视频进行缩放
@app.route('/scale_video/<int:num>')
def scale_video(num):
    cam.scale_video(num)
    return redirect(url_for('current_video'))

# 对视频质量进行缩放
@app.route('/quality_video/<int:num>')
def quality_video(num):
    cam.quality_video(num)
    return redirect(url_for('current_video'))

# 对视频的设置进行重置
@app.route('/reset_video/')
def reset_video():
    cam.reset_video()
    return redirect(url_for('current_video'))

# 读取所有照片
@app.route('/pic_list/')
def pic_list():
    piclist = cam.get_all_picture()
    return render_template('pic_list.html',piclist=piclist)

# 删除制定对应图片
@app.route('/del_pic/<name>')
def del_pic(name):
    cam.del_pic(name)
    return redirect(url_for('pic_list'))

@app.route('/video_feed')
def video_feed():
    return Response(cam.gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 读取指定的markdown文件,然后转成html显示
@app.route('/about/<name>')
def about(name):

    file_object = open(os.getcwd() + '/static/md/' +name + '.md')
    try:
         all_the_text = file_object.read( )

    finally:
         file_object.close()
    htmltext = markdown2.markdown(all_the_text)
    return render_template('about.html',text= htmltext)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
