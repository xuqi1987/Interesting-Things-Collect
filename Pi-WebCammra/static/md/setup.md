## 功能说明
1. 使用http mimetype为multipart/x-mixed-replace报文，实现在线视频（服务器推送(Server Push) ）
2. 通过将图片保存文件实现拍照功能。
3. 读取整个目录下的所有图片，显示图片并且可以对图片进行删除
4. 使用markdown2，读取目录下的md文件，然后转换成html显示在网页上。

## 目录结构

![](http://cl.ly/3g3C1c0U3f1p/Image%202016-02-27%20at%2012.45.53%20%E4%B8%8B%E5%8D%88.png)

### 文件说明：

layout.html
所有页面的基类,主要包括一个导航栏

camera_layout.html
模板中包括几个功能button

video_push.html
用来显示视频

current_picture.html
显示拍照

app.py
定义各种路由

camera.py
和摄像头操作有关的类。

### 关键技术说明

```
＃取得设备编号为0的
import cv2
cap = cv2.VideoCapture(0)

＃读取图片Frame
ret,frame = cap.read()

# 将图片解码，转换成string
strframe = cv2.imencode('.jpg', frame)[1].tostring()

# 将strframe 写入文件
file_object = open('pystream/pic/test.jpg', 'w')
file_object.write(strframe)
file_object.close()

# 将frame 转换成NumPy的数组
in_img = image.fromarray(frame)

# 对图片进行大小调整
in_img.resize((newWidth,newHeight),image.ANTIALIAS)

```
服务器推送(Server Push) 技术详解

```
# 设置图片的路径后，会重新发起一次http get 方法
<img src="{{ url_for('video_feed') }}" class="img-thumbnail center-block">
```

通过chrome可以看到Response Header为：

```
HTTP/1.0 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame
Connection: close
Server: Werkzeug/0.11.3 Python/2.7.10
Date: Sat, 27 Feb 2016 14:10:47 GMT

```
大致流程是：
使用telnet 测试

```
xuqitekiMacBook-Air:pystream xuqi$ telnet
telnet> open 192.168.1.114 5000
Trying 192.168.1.114...
Connected to 192.168.1.114.
Escape character is '^]'.
GET /video_feed HTTP/1.0
Host:192.168.1.114

```

Response 结果

```
HTTP/1.0 200 OK
Content-Type: multipart/x-mixed-replace; boundary=frame
Connection: close
Server: Werkzeug/0.11.4 Python/2.7.9
Date: Sun, 14 Feb 2016 02:29:33 GMT

--frame
Content-Type: image/jpeg

JFIFC



第一张图片的数据
--frame
Content-Type: image/jpeg

JFIFC


第二张图片的数据
--frame

```

实现方法

```
@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen():
	...
	yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
```
### 问题（不明白）
1. Mac上Flask无法设置多个progress
2. Raspberry不能开启debug=True

### 待解决问题

1.Raspberry上会出现Error

```
  File "/usr/lib/python2.7/SocketServer.py", line 295, in _handle_request_noblock
    self.process_request(request, client_address)
  File "/usr/lib/python2.7/SocketServer.py", line 321, in process_request
    self.finish_request(request, client_address)
  File "/usr/lib/python2.7/SocketServer.py", line 334, in finish_request
    self.RequestHandlerClass(request, client_address, self)
  File "/usr/lib/python2.7/SocketServer.py", line 657, in __init__
    self.finish()
  File "/usr/lib/python2.7/SocketServer.py", line 716, in finish
    self.wfile.close()
  File "/usr/lib/python2.7/socket.py", line 279, in close
    self.flush()
  File "/usr/lib/python2.7/socket.py", line 303, in flush
    self._sock.sendall(view[write_offset:write_offset+buffer_size])
error: [Errno 32] Broken pipe

```
可能原因是因为是
如果客户端在服务器返回前，主动断开连接，则服务器端会报 [Errno 32] Broken pipe 错，并导致处理线程 crash.
没找到解决办法。

2.Raspberry 经常锁死，一直在走循环



