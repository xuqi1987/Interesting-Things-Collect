#! /usr/bin/python
# -*- coding:utf-8 -*-
from sensor import Sensor

import time
se = Sensor()
se.setup()
try:
    while True:
        se.get()
        time.sleep(1)
except KeyboardInterrupt:
    se.destory()