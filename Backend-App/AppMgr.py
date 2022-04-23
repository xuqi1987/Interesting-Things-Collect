# -*- coding: utf-8 -*-

import time


from common.tools import *
from movieflask.movie import startresetful
import os
from weixinflask.weixin import startweixin
from celery_app.task_movie import scrapy_movie
from database.datamodule import create_init_table
from common.config import getweixin_port,getmovie_port

if __name__ == '__main__':

    try:
        # init sqlite3 database
        create_init_table()

        # start celery
        Run("celery -B -A celery_app worker --loglevel=warning","启动celery",kill=True)

        scrapy_movie.delay('hdwan')

        # run weixin flask
        Run("gunicorn -w4 -b0.0.0.0:%s weixinflask.weixin:weixin_app"%getweixin_port(),"Weixin Server",kill=True)
        # run movie flask
        Run("gunicorn -w4 -b0.0.0.0:%s movieflask.movie:movie_app"%getmovie_port(),"Movie Server",kill=True)

        while True:
            time.sleep(36000)
            pass
        #Run("gunicron -w4 -b0.0.0.0:5003 myapp:app")

        # function_list=  [startresetful, startweixin]
        # print "主程序进程id: %s" %(os.getpid())
        # pool=multiprocessing.Pool(2)
        # for func in function_list:
        #     pool.apply_async(func)

        # pool.close()
        # pool.join()


    except (KeyboardInterrupt, SystemExit):
        # 异常退出,关闭用run启动的进程

        KillAll()
