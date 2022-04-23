# -*- coding: utf-8 -*-

from datetime import timedelta
from celery.schedules import crontab
from common.config import getceleryip,getceleryport
# Broker and Backend
#BROKER_URL = 'redis://x2020.top:6379'
#CELERY_RESULT_BACKEND = 'redis://x2020.top:6379/0'


BROKER_URL = 'redis://%s:%s'%(getceleryip(),getceleryport())
CELERY_RESULT_BACKEND = 'redis://%s:%s/0'%(getceleryip(),getceleryport())

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'
# CELERY_TIMEZONE='UTC'

# import
CELERY_IMPORTS = (
    'celery_app.task_movie',
)

# schedules
CELERYBEAT_SCHEDULE = {
    # 'add-every-30-seconds': {
    #      'task': 'celery_app.task_movie.test',
    #      'schedule': timedelta(seconds=30),       # 每 30 秒执行一次
    #      'args': (5, 8)                           # 任务函数参数
    # },

    'scrapy-at-0-clock-time': {
        'task': 'celery_app.task_movie.scrapy_movie',
        'schedule': crontab(hour=0, minute=0),   # 每天早上 0 点 0 分执行一次
        'args': 'hdwan'                            # 任务函数参数
    }
}