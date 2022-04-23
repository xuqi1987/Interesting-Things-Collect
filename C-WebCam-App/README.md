# 17.webcam_c

参考链接：
[http://blog.chinaunix.net/uid-20746260-id-4048699.html]()

想了解v4l2读取读取摄像头，然后encode进行传输，decode显示，在网上找到了sunkwei的一个可以参考的例子《基于v4l2的webcam应用, 本地预监》，原文地址http://blog.csdn.net/sunkwei/article/details/6530343，在Ubuntu12.04LTS上进行了初步测试，源代码可在如下地址下载：
  http://download.csdn.net/detail/sunkwei/3425209  
    另外参考了kangear的另一篇博客《基于v4l2的webcam应用, 本地预监(编译过程)》，原文地址
http://blog.csdn.net/kangear/article/details/8721068

测试步骤如下：

1. 安装ffmpeg环境，命令：sudo apt-get install ffmpeg
2. 安装libavcodev-dev ,命令:sudo apt-get install libavcodec-dev
3. 安装libswscale-dev,命令：sudo apt-get install libswscale-dev
4. 安装libx264-dev, 命令：sudo apt-get install libx264-dev
5. 修改/usr/include/libavutil/common.h, 添加如下内容。（否则会报c与c++兼容问题）

```
#ifndef UINT64_C 
#define UINT64_C(value)__CONCAT(value,ULL) 
#endif

```
6.至此编译程序，会出现错误x11/xlib.h nosuch file or directory
解决方法：
先安装X11，命令为sudo apt-get install libx11-dev
sudo apt-cache search x11-dev，结果如下：
```
libgl1-mesa-swx11-dev - free implementation of the OpenGL API -- development files
libx11-dev - X11 client-side library (development headers)
libghc-x11-dev - Haskell X11 binding for GHC
libghc6-x11-dev - transitional dummy package
```
以此安装以上软件包：
```
sudo apt-get install libghc6-x11-dev
sudo apt-get install libghc-x11-dev
sudo apt-get install libx11-dev
sudo apt-get install libgl1-mesa-swx11-dev
```

**编译测试：**

在webcam下执行make
    # cd webcam
    # make
编译可得到服务器端和客户端的应用程序  webcam_server和  webcam_shower
测试：
在一个终端执行./webcam_server，开启另一个终端执行./webcam_shower，结果如下：