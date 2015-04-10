#!/bin/env python2.7
#-*- coding=utf-8 -*_
 
"""
Author: 周宸翰 Hank
Date: 2014-12-26 11:13:18
任务操作
"""
 
import sys, time, os, random, signal, Queue
from Loger    import Loger
from TaskDistribute import TaskDistribute
from TaskDistribute import tryProducer
from config   import config

#获取此脚本位置,所有路径主入口-----------------------------------
FILE_PATH, APP_NAME = os.path.split(os.path.abspath(sys.argv[0]))
APP_PATH = FILE_PATH + '/../'
KEY_PATH = APP_PATH + '/keytemp/'
CFG_PATH = APP_PATH + '/conf' + '/hosts'
#---------------------------------------------------------------

if __name__ == '__main__':
    #调用log函数
    Log = Loger(APP_PATH)
    #new queue
    queue = Queue.Queue(0)
    #设置线程池
    td = TaskDistribute(Loger=Log, Thread_cores=5, newQueue=queue)
    #添加测试生产者
    tp = tryProducer(Loger=Log, newQueue=queue, maxId=20)
    #监控信号
    signal.signal(signal.SIGINT, td.stop)
    signal.signal(signal.SIGTERM, td.stop)
    #开始测试生产
    tp.start()
    Log.D("主函数生产者灌入等待2S")
    time.sleep(1)
    #开始进行程序
    reData = td.run()
