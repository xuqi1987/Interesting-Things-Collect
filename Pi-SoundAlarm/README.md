## Android报警

基本结构参照：
git@git.oschina.net:xuqi1987/Android.git

### 创建虚拟环境

	mkvirtualenv raspberry

### 安装Flask
	
	pip install Flask
	
### 安装 GPIO
	
	pip install rpi.gpio

#### 看引脚的方式：

![](http://cl.ly/3k0L373q213E/Image%202016-03-19%20at%203.31.20%20%E4%B8%8B%E5%8D%88.png)

#### 引脚图：

![](http://cl.ly/0G0g2r3l1E3i/Image%202016-03-19%20at%204.01.31%20%E4%B8%8B%E5%8D%88.png)

口哨传感器的ACC，GND，OUT连接树莓派物理引脚的4，6，8，其中引脚8对应的BCM为GPIO14。

### 客户端 （Android）

监听线程

```
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        System.out.println("onStartCommand");
        new Thread() {
            @Override
            public void run() {
                super.run();
                int i =0;
                while(isRunning) {
                    i++;

                    Map map = NetUtil.checkPi(url);

                    String st = map.get("id").toString();
                    if (st.equals("true")) {
                        if (!playsound) {
                            playSound();
                            playsound = true;
                        }
                    } else {
                        stopSound();
                        playsound = false;
                    }

                    //System.out.println("hello");
                    try {
                        sleep(3000);
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }

                }


            }
        }.start();
        return super.onStartCommand(intent, flags, startId);
    }
```

```

    public static Map checkPi(String url) {
        System.out.println("checkPi " + url);
        String result = null;
        Map params = new HashMap();//请求参数
        Map data = new HashMap();
        try  {
            result = net(url,params,"GET");
            data = toMap(result);
        }catch (Exception e) {
            e.printStackTrace();
        }
        return data;
    }
    
```

服务器端

```
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

```


效果图：

![](http://cl.ly/3n2I2Y0l0Y1h/Image%202016-03-20%20at%203.52.34%20%E4%B8%8B%E5%8D%88.png)







