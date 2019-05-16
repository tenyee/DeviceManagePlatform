#!/usr/bin/python3
import threading
from multiprocessing import Pool, Process, Queue
import multiprocessing
import os, time, random

'''
参考：
1。日志模块:https://www.cnblogs.com/CJOKER/p/8295272.html
'''

#全局lock
threadLock = threading.Lock()
    
def Lock():
   threadLock.acquire()
       
def UnLock():
   threadLock.release()
       
# 线程类
class SimpleThread(threading.Thread):
    """
       创建简单的线程类
       入参:
       threadID:线程id
       name    :线程名
       func    :执行函数
       param   :函数参数，是一个dict
    """
    def __init__(self, threadID, name, func, param = None):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.func = func
        self.param = param
        
    def run(self):
        print ("[" + time.ctime(time.time()) + "]开始线程：" + self.name)
        self.func(self.param)
        print ("[" + time.ctime(time.time()) + "]退出线程：" + self.name)

# 数据分类
def ClassifyData(rawData, tagData, quickData, slowData, normalData):
   otherData = rawData["otherData"]
   
   for item in otherData:
      tag = tagData[item["dev_ip"]]
      if tag == "slow":
         slowData.append(item)
      else:
         normalData.append(item)

   #quickData中可能存在慢数据，去掉
   for item in rawData["quickData"]:
      tag = tagData[item["dev_ip"]]
      if tag == "slow":
         slowData.append(item)
      else:
         quickData.append(item)
         
# 数据分发
def distributeTask(data, dataQueue, putWhatever = True):
   if putWhatever == True:
      try:
         for item in data:
            dataQueue.put(item, timeout = 2)
      except Exception as e:
            pass
   else:
      #队列数据少于10个时，直接压入
      if dataQueue.qsize() < 10:
         for item in data:
            try:
               dataQueue.put(item, timeout = 2)
            except Exception as e:
               pass
   
# pull进程：负责拉取数据，并进行分流
def PullTaskProcess(param):
   """
   功能：秒级轮询数据
   param是一个dict
   """
   url         = param["url"]
   quickQueue  = param["quickQueue"] #快速队列，用于传送实时请求到处理进程
   slowQueue   = param["slowQueue"]  #慢速队列，用于传送慢速处理进程
   normalQueue = param["normalQueue"]#常规队列
   tagData     = param["tagData"]#数据标签，用于分流，由各进程更新
   watchDog    = param["watchDog"]
   while True:
      #1.获取数据
      try:
         rawData    = http_get()
      except Exception as e:
         pass
      else:
         #2.数据分流
         quickData  = []
         slowData   = []
         normalData = []
         ClassifyData(rawData, tagData, quickData, slowData, normalData)
         #3.分发
         distributeTask(quickData, quickQueue)
         distributeTask(slowData, slowQueue, putWhatever = False)
         distributeTask(normalData, normalQueue, putWhatever = False)
      finally:
         watchDog["PullTaskProcess"] = 1 #主进程里定时把它置为0，如果检测到指定连续N次还是0的时，会重启进程

def QuickTaskProcess(param):
   quickQueue  = param["quickQueue"] #快速队列，用于传送实时请求到处理进程
   tagData     = param["tagData"]#数据标签，用于分流，由各进程更新
   watchDog   = param["watchDog"]
   print("#QuickTaskProcess start#")
   while True:
      try:
         pass
      except Exception as e:
         pass
      else:
         pass
      finally:
         watchDog["QuickTaskProcess"] = 1 #主进程里定时把它置为0，如果检测到指定连续N次还是0的时，会重启进程
         time.sleep(30)

def SlowTaskProcess(param):
   slowQueue  = param["slowQueue"] #快速队列，用于传送实时请求到处理进程
   tagData     = param["tagData"]#数据标签，用于分流，由各进程更新
   watchDog   = param["watchDog"]
   
   while True:
      try:
        pass
      except Exception as e:
        pass
      else:
        pass
      finally:
         watchDog["SlowTaskProcess"] = 1 #主进程里定时把它置为0，如果检测到指定连续N次还是0的时，会重启进程
         time.sleep(1)

def NormalTaskProcess(param):
   normalQueue  = param["normalQueue"] #快速队列，用于传送实时请求到处理进程
   tagData     = param["tagData"]#数据标签，用于分流，由各进程更新
   watchDog   = param["watchDog"]
   
   while True:
      try:
         pass
      except Exception as e:
         pass
      else:
         pass
      finally:
         watchDog["NormalTaskProcess"] = 1 #主进程里定时把它置为0，如果检测到指定连续N次还是0的时，会重启进程
         tagData["NormalTaskProcess"] += 1
         time.sleep(1)

##########################################################################
#                     线程测试
##########################################################################
# 线程测试用例
def func1(param):
   snap = param["snap"] if param["snap"] != None else 0
   count = param["count"] if param["count"] != None else 5
   while count > 0:
      time.sleep(snap)
      print("func1:" , count)
      count -= 1
      
def func2(param):
   snap = param["snap"] if param["snap"] != None else 0
   count = param["count"] if param["count"] != None else 5
   while count > 0:
      time.sleep(snap)
      print("func2:" , count)
      count -= 1
      if count == 3:
         t1.terminate()

# 线程测试用例
def thread_test():
   # 创建新线程
   thread1 = SimpleThread(10996, "Thread-1", func1, {"snap":2, "count":1000})
   thread2 = SimpleThread(20996, "Thread-2", func2, {"snap":2, "count":1000})

   # 开启新线程
   thread1.start()
   thread2.start()
   thread1.join()
   thread2.join()
   print ("退出主线程")
##########################################################################

def process_test():
   #创建三个队列
   manager = multiprocessing.Manager()
   quickQueue  = manager.Queue(maxsize = 50)
   slowQueue   = manager.Queue(maxsize = 100)
   normalQueue = manager.Queue(maxsize = 100)
   
   #构造数据
   param = multiprocessing.Manager().dict()  #创建主进程与子进程共享
   param["quickQueue"]                   = quickQueue
   param["slowQueue"]                    = slowQueue
   param["normalQueue"]                  = normalQueue
   param["tagData"]                      = manager.dict()
   param["watchDog"]                     = manager.dict()
   param["tagData"]["PullTaskProcess"]   = 0
   param["tagData"]["QuickTaskProcess"]  = 0
   param["tagData"]["SlowTaskProcess"]   = 0
   param["tagData"]["NormalTaskProcess"] = 0
   param["watchDog"]["PullTaskProcess"]  = 0
   param["watchDog"]["QuickTaskProcess"] = 0
   param["watchDog"]["SlowTaskProcess"]  = 0
   param["watchDog"]["NormalTaskProcess"]= 0
   
   #创建四个子进程
   #pullProcess   = Process(target = PullTaskProcess,   args = ())
   quickProcess  = Process(target = QuickTaskProcess,  args = (param,))
   slowProcess   = Process(target = SlowTaskProcess,   args = (param,))
   normalProcess = Process(target = NormalTaskProcess, args = (param,))
   
   quickProcess.start()
   slowProcess.start()
   normalProcess.start()
   
   count = {}
   count["QuickTaskProcess"]   = 0
   count["SlowTaskProcess"]    = 0
   count["NormalTaskProcess"]  = 0
   while True:
      time.sleep(1)
      print("---main---")
      print("watchDog:", param["watchDog"])
      print("tagData:", param["tagData"])
      print("---main---")
      
      if param["watchDog"]["QuickTaskProcess"] == 0:
         count["QuickTaskProcess"] += 1
      elif param["watchDog"]["SlowTaskProcess"] == 0:
         count["SlowTaskProcess"] += 1
      elif param["watchDog"]["NormalTaskProcess"] == 0:
         count["NormalTaskProcess"] += 1

      param["watchDog"]["QuickTaskProcess"] = 0
      param["watchDog"]["SlowTaskProcess"] = 0
      param["watchDog"]["NormalTaskProcess"] = 0
      
      print('count["QuickTaskProcess"]=',count["QuickTaskProcess"])
      
      if quickProcess.is_alive():
         print("live")
      else:
         print("not live, restert")
         quickProcess.start()
         
      if count["QuickTaskProcess"] >= 5:
         try:
            count["QuickTaskProcess"] = 0
            quickProcess.terminate()

            time.sleep(1)
            quickProcess = Process(target = QuickTaskProcess,  args = (param,))
            quickProcess.start()
            print("restart QuickTaskProcess")
         except Exception as e:
            print("@#$%ˆ&*(:", str(e))


if __name__ == "__main__":
   process_test()