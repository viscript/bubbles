#!/bin/env python2.7
#-*- coding=utf-8 -*_

"""
Author: 周宸翰 Hank
Date: 2014-12-22 12:13:18
Bubbles 多线程处理
"""
import Queue, threading, time, random

def doJob(strr, id=0):
    #time.sleep(random.uniform(0, 1))
    print "     ** " + strr + " Task ID: " + str(id) + "完成**"

#生产者测试使用
class tryProducer(threading.Thread):
    def __init__(self, Loger, newQueue, funciton=doJob, maxId=100):
        threading.Thread.__init__(self)
        self.queue = newQueue
        self.maxId = maxId
        self.L = Loger
        self.L.D("生产者初始化完成")
        self.function = doJob

    def run(self):
        indexx = 0
        while indexx < self.maxId:
            time.sleep(0.05)
            argss = {}
            argss['strr'] = 'test'
            argss['id'] = indexx
            self.L.I("任务队列添加: " + self.function.__name__ + " 参数: " + argss.__str__())
            self.queue.put((self.function, argss)) 
            indexx=indexx+1
        self.L.D("生产者队列长度暂时为: " + str(self.queue.qsize()))
       
class monitorT(threading.Thread):
    def __init__(self, thread_Max_time, Loger): 
        threading.Thread.__init__(self)
        self.thread_Max_time = thread_Max_time
        self.L = Loger

    def run(self):
        global monitor
        while True:
            time.sleep(0.5)
            for th in monitor:
                try:
                    sub_time = int(time.time() - monitor[th]['start'])
                    self.L.D("线程: " + th + " 正在运行时间: " + str(sub_time) )
                    if int(sub_time) > self.thread_Max_time:
                        self.L.D("线程: " + th + " 超时")
                        monitor[th]["status"] = "timeout"
                    pass
                except NameError:
                    pass
       

 
class MyThread(threading.Thread):
    def __init__(self, queue, reQueue, thread_number, thread_cores, task_count, Loger):
        threading.Thread.__init__(self)
        self.queue = queue
        self.reQueue = reQueue
        self.thread_number = thread_number
        self.thread_cores = thread_cores
        self.task_count = task_count
        self.L = Loger
        self.do_that = True
        self.L.D("线程ID: " + str(self.thread_number) + " 初始化完成")

    def stop(self):
        self.do_that = False
        self.L.I("线程ID: " + str(self.thread_number) + " 接受线程停止信号(2/2).")

    def run(self):
        global monitor
        while True:
            #time.sleep(0.01)
            if self.do_that == True and self.queue.qsize() > 0 :
                try:
                    count = monitor[self.getName()]['count']
                    monitor[self.getName()]={'start':time.time(),'count':count+1, 'thread': self, "status":"active"}
                    self.L.D(monitor[self.getName()])
                except KeyError:
                    monitor[self.getName()]={'start':time.time(),'count':0, 'thread':self, "status":"active"}
                    self.L.D(monitor[self.getName()])
                function, args = self.queue.get()
                self.L.I("函数: " + function.__name__ + " 参数: " + args.__str__() + ", 现在任务处理线程ID: " + str(self.thread_number))

                reData = function(**args)
                self.L.I("函数: " + function.__name__ + " 参数: " + args.__str__() + ", 任务处理线程ID: "     + str(self.thread_number) + " 任务完成")
                self.reQueue.put((reData,args))
            #elif self.do_that == False and self.queue.qsize() > 0:
            #    function, args = self.queue.get()
            #    #pass
            else:
                time.sleep(1)
                try:
                    count = monitor[self.getName()]['count']
                    monitor[self.getName()]={'start':time.time(), 'count':count, 'thread':False, "status":"idle"}
                    self.L.D(monitor[self.getName()])
                except KeyError:
                    monitor[self.getName()]={'start':time.time(), 'count':0, 'thread':False, "status":"idle"}
                    self.L.D(monitor[self.getName()])

class TaskDistribute():
    def __init__(self, Loger, 
                       Thread_cores=4,
                       newQueue=Queue.Queue(0)):
        self.L = Loger
        self.queue = newQueue
        self.reQueue = Queue.Queue(0)
        self.threads_list = []
        self.Thread_cores = Thread_cores
        self.Id_counter = 0
        self.do_that = True
        self.L.D("线程池类初始化完成")

    def addArgs(self, function, **args):
        self.L.I("任务队列添加: " + function.__name__ + " 参数: " + args.__str__())
        self.queue.put((function, args)) 

    def stop(self, signum, frame):
        self.do_that = False
        self.L.I("触发线程停止信号(1/2).")
        
    def run(self):
        self.L.I("任务数量: " + str(self.queue.qsize()))
        global monitor
        #monitor 线程状态
        #{"thread-2":{"start":3.21212121, "count": 3, "thread":function, "status":"active/timeout/idle"}}
        monitor = {}
        mt = monitorT(thread_Max_time=3, Loger=self.L)
        mt.start()
        while True:
            #time.sleep(0.01)
            timeout_num = 0
            if self.do_that == True:
                for th in monitor:
                    if "timeout" in monitor[th]['status']:
                        timeout_num+=1
                if  self.queue.qsize() > 0 and  (threading.activeCount() - 1) < self.Thread_cores + timeout_num:
                    thread = MyThread(queue = self.queue, 
                                      reQueue = self.reQueue,
                                      thread_number = self.Id_counter, 
                                      thread_cores = self.Thread_cores,
                                      task_count = self.queue.qsize(),
                                      Loger = self.L)
                    self.Id_counter += 1
                    self.threads_list.append(thread)
                    thread.start()
                #为了生产生消耗者模型屏蔽直接列队为0退出
                #else:break
                elif self.queue.qsize() > 0:
                    self.L.I("队列不为空,线程资源耗尽等待运行线程执行完毕")
                    time.sleep(0.5)
                else:
                    self.L.I("队列为空,等待队列添加...")
                    time.sleep(0.5)
            else:
                self.L.I("手动停止任务队列.")
                for thread in self.threads_list:
                    thread.stop()
                for thread in self.threads_list:
                    thread.join()
                break
        for thread in self.threads_list:
            thread.join()
        self.L.I("任务队列完成.")
        return self.reQueue
