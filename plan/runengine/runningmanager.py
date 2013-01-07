#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from atplatform.plan.runengine import execute
import time
from multiprocessing import Process,Queue,Value, Array
import thread
#import runninginfo
from types import *
import atplatform.plan.sharedobject as so
import functools
import atplatform.plan.commonparam as cp
import threading
import traceback
from atplatform.plan.runengine.runqueue import runqueue
try:
	from atplatform.plan.mappedtable import *
except:
	pass

def exceptioncatchcommon(func):
	@functools.wraps(func)
	def wrappedFunc(*arg,**argd):
		try:
			return func(*arg,**argd)
		except Exception, e:
			so.runmanagerlog.error('call function ['+func.func_name+'] error,raw traceback info: '+traceback.format_exc())
			return False
	return wrappedFunc

class runningmanager(object):
	#global runninginfo
	"""docstring for runningmanager"""
	#workerinfo {status,'failed',errormsg,pic}
	def __init__(self):
		super(runningmanager, self).__init__()
		self.runningworker={}		#具体执行任务的worker，key-value，value为worker句柄
		self.stoppedworker=[]		#已经停止的worker，正常停止
		self.deadworker=[]			#已经停止的worker，异常停止
		self.workerinfo={}			#workerinfo，[状态，时间(float)，res]，成功：[状态，开始时间,结束时间,'success','',''],失败：[状态，开始时间,结束时间,'failed',错误信息,错误发生时的截图图片]
		self.finishedworkercount=0				#执行完的worker数量
		self.pushqueuecount=0			#当前plan push用例队列深度
		self.waitingqueue=[]		#在达到此plan的最大并发执行数后，其他任务将存入等待push队列
		self.stopflag=False			#停止信号标示
		self.webdrivercollection={} #每个worker对应的webdriver
		self.planhandler=None		#用来调用plan方法的句柄
#		runninginfo.runningmanagerlist.append(self)		#添加此runningmanager对象进入runninginfo
		self.newlock = threading.RLock()  #新建worker和停止所有worker的竞争锁
		self.msgcontainer={}					#若driver获取到了最终结果，那么将此结果发送至结果收端
		#thread.start_new_thread(self.gggg,())

	# def gggg(self):
	# 	while 1:
	# 		print "queuelength::::::"+str(len(runqueue.queue))
	# 		time.sleep(5)

	#@exceptioncatchcommon
	def newworker(self,casename,config):
		self.newlock.acquire()
		if self.stopflag!=True:
			q=Queue()
			name=(casename+"__"+time.strftime("%Y-%m-%d__%H.%M.%S", time.localtime()).replace(':','.')).decode('gbk').encode('utf8')
			self.workerinfo[name]=[so.workerstatus[0],0,0,'','','']
			if self.pushqueuecount<cp.maxpush:
				#_dict=['planname',(name,runmanagerinstance_self,casename.config.q)]
				_dict=[self.planhandler.name,(name,self,casename,config,q)]
				runqueue.push(_dict,self)
				so.runmanagerlog.debug('push case:'+casename+' in config:'+str(config)+' to manager runlist,planname:'+self.planhandler.name)
			else:
				self.waitingqueue.append([name,casename,config,q])  #存入等待队列，不会进行push
				so.runmanagerlog.debug('push case:'+casename+' in config:'+str(config)+' to manager waitlist,planname:'+self.planhandler.name)
				self.workerinfo[name]=[so.workerstatus[4],0,0,'','','']
			self.newlock.release()
			time.sleep(1)	#单个plan最短push间隔至少1秒
			return name
		else:
			newlock.release()
			return None

	def killworker(self,name):
		so.runmanagerlog.debug('killworker start:'+name)
		self.runningworker[name].terminate()
		so.runmanagerlog.debug('killworker end:'+name)
		self.deadworker.append(name)
		self.runningworker.pop(name)
		self.workerinfo[name][0]=so.workerstatus[3]

	@exceptioncatchcommon
	def killallworkers(self):
		self.stopflag=True
		self.newlock.acquire()
		for i in self.runningworker.keys():
			self.killworker(i)
		so.runmanagerlog.info('all workers stoped,plan:'+self.planhandler.name)
		self.newlock.release()

	#必须在killallworkers或全停止并发送结果后才能clear
	def clear(self):
		self.runningworker.clear()
		self.stoppedworker=[]
		self.deadworker=[]
		self.workerinfo.clear()
		self.finishedworkercount=0
		self.pushqueuecount=0
		self.waitingqueue=[]
		self.stopflag=False
		self.webdrivercollection.clear()
		self.msg={}

	@exceptioncatchcommon
	def flushrunmanager(self):
		self.waitingqueue=[]
		self.killallworkers()
		time.sleep(20)
		self.clear()
		so.runmanagerlog.info('runmanager has been flushed,plan:'+self.planhandler.name)

	@exceptioncatchcommon
	def __jointhread__(self,name,p,queue):
		thread.start_new_thread(self.__getrunningdriver,(name,queue))
		p.join()
		so.runmanagerlog.info('one case thread has finished,case:'+name+',plan:'+self.planhandler.name)
		if self.stoppedworker.count(name)==0:
			self.stoppedworker.append(name)
		if self.runningworker.has_key(name):
			self.runningworker.pop(name)
		try:
			res= queue.get(timeout=5)
		except Exception, e:
			if self.msgcontainer.has_key(name):
				res=self.msgcontainer.pop(name)
			else:
				res=['failed','getresultfailed','']
				so.runmanagerlog.error('get result failed,case:'+name+',plan:'+self.planhandler.name)
		try:
			self.webdrivercollection[name].quit()
			self.webdrivercollection.pop(name)
		except Exception, e:
			pass
		if self.stopflag!=True:
			if self.workerinfo[name][0]!=so.workerstatus[3]:
				self.workerinfo[name][0]=so.workerstatus[2]
			self.setworkerinfo(name,res)
			if self.finishedworkercount==len(self.planhandler.plancases) and self.stopflag!=True:
				self.planhandler.finishedtocall()
			self.pushqueuecount=self.pushqueuecount-1
			so.runmanagerlog.info('pushqueuecount -1,length:'+str(self.pushqueuecount)+' plan:'+str(self.planhandler.name))
			if len(self.waitingqueue)>0:
				try:
					case=self.waitingqueue.pop(0)
					_dict=[self.planhandler.name,(case[0],self,case[1],case[2],case[3])]
					runqueue.push(_dict)  #一个worker执行完毕后再push一个worker
					so.runmanagerlog.info('push another case to runqueue,case:'+str(case[0])+',plan:'+str(self.planhandler.name))
				except Exception,e:
					so.runmanagerlog.error('error occured during push a new case to runqueue,plan:'+str(self.planhandler.name))
		runqueue.runningqueuelength=runqueue.runningqueuelength-1
		so.runmanagerlog.info('runningqueuelength -1 ,length:'+str(runqueue.runningqueuelength)+' from plan:'+str(self.planhandler.name))


	def __getrunningdriver(self,name,queue):
		try:
			msg=queue.get(timeout=30)
			from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver
			if isinstance(msg,RemoteWebDriver):
				self.webdrivercollection[name]=msg
			else:
				self.msgcontainer[name]=msg
		except Exception, e:
			so.runmanagerlog.warning('get webdriver failed,name:'+str(name)+',plan:'+str(self.planhandler.name))

	@exceptioncatchcommon
	def setworkerinfo(self,name,res):
		self.workerinfo[name][3:]=res
		self.workerinfo[name][2]=time.time()
		self.finishedworkercount=self.finishedworkercount+1
		so.runmanagerlog.info('finishedworkercount +1 ,case:'+str(name)+',plan:'+str(self.planhandler.name))

