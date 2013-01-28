#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from atplatform.plan.runengine.runningmanager import *
from atplatform.plan.runengine import execute
import gc
import traceback
from atplatform.plan.runengine import runninginfo
import sys
import functools
import thread
import sched
import time
import os
import pika
import shutil
import atplatform.plan.commonparam as cp
import atplatform.plan.sharedobject as so
import re
try:
	from atplatform.plan.mappedtable import *
except:
	pass

planhandlers={}

def exceptioncatchcommon(func):
	@functools.wraps(func)
	def wrappedFunc(*arg,**argd):
		try:
			return func(*arg,**argd)
		except Exception, e:
			so.planprogresslog.error('call function ['+func.func_name+'] error,raw traceback info: '+traceback.format_exc())
			return False
	return wrappedFunc


#name=rm.newworker('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'})
class plan(object):
	"""docstring for plan"""
	def __init__(self):
		super(plan, self).__init__()
		self.name=""    				#planname
		self.planstarttime = [0,0]     	#planstarttime，参数：第一个，计时器执行方式；第二个，由第一个参数确定的具体值，例如1对应+1111,2对应12:00
		self.plancases={}              	#cases in this plan
		self.runningmanager=None		#runengine in this plan
		self.status=""					#plan当前状态
		self.stopflag=False				#plan停止信号标示
		self.s = sched.scheduler(time.time, time.sleep)			#为此plan实例添加定时器对象
		self.plantimeinfo=[0,0,0]  		#计划制定时间、开始时间、执行结束时间

	@exceptioncatchcommon
	def setplanstarttime(self,_time=None):
		if _time!=None:
			if (_time[0]=='+' and _time[1:].isdigit() and int(_time[1:]) >=0):
				self.planstarttime=[1,int(_time[1:])]
				self.plantimeinfo[0]=time.time()
				self.plantimeinfo[1]=self.plantimeinfo[0]+int(_time[1:])
			else:
				dsttime=time.mktime(time.strptime(_time, '%Y %m %d %H %M %S'))
				if time.time()>dsttime-5:   #设置计划时间时的时间必须小于计划时间5秒
					return False
				self.planstarttime=[2,dsttime]
				self.plantimeinfo[0]=time.time()
				self.plantimeinfo[1]=dsttime
		return True

	def setplancases(self,caseslist):
		self.plancases=caseslist
		self.status=so.planstatus[0]
		self.__setplanstatus(so.planstatus[0])

	#@exceptioncatchcommon
	def run(self):
		try:
			so.runmanagerlog.info('start a runmanager for plan:'+self.name)
			self.runningmanager=runningmanager()
			self.runningmanager.planhandler=self 			#将plan句柄给runengine，用来在runengine执行完毕时传递回信息
			if self.planstarttime[0] ==0:
				self.s.enter(0,1,self.__run,())
			else:
				if self.planstarttime[0]== 1:
					self.s.enter(self.planstarttime[1],1,self.__run,())
				else:
					self.s.enterabs(self.planstarttime[1],1,self.__run,())
			self.status=so.planstatus[1]
			self.__setplanstatus(so.planstatus[1])
			thread.start_new_thread(self.__checkrun,())			#开一个线程监视计划的工作开始时更改plan状态
			so.runmanagerlog.info('runmanager has been ready ,wait to run,plan:'+self.name)
		except Exception,e:
			so.runmanagerlog.error('error occured during start the sched process and push tasks'+traceback.format_exc())
			for i in self.s.queue:
				self.s.cancel(i)
			raise Exception(traceback.format_exc())

	@exceptioncatchcommon
	def __checkrun(self):
		self.s.run()
		self.status=so.planstatus[2]
		self.__setplanstatus(so.planstatus[2])
		so.runmanagerlog.info('runmanager has started to run,plan:'+self.name)

	@exceptioncatchcommon
	def checkstatus(self):
		finishcases=float(0)
		if self.runningmanager==None and self.status==so.planstatus[3]:
			finishcases=float(len(self.plancases))
		else:
			if self.runningmanager==None and self.status!=so.planstatus[3]:
				finishcases=float(0)
			else:
				finishcases=float(self.runningmanager.finishedworkercount)
		if len(self.plancases)!=0:
			return self.status,[finishcases,float(len(self.plancases))]
		else:
			return False

	#@exceptioncatchcommon
	def __run(self):
		try:
			for caseinfo in self.plancases:
				self.runningmanager.newworker(caseinfo[0],caseinfo[1])
		except Exception,e:
			so.planprogresslog.error('error occured during start the runningmanager task,planname: '+self.name+',traceback:'+traceback.format_exc())
			so.planprogresslog.debug('start to forcestop plan:'+self.name)
			res=self.forcestop()
			if res==True:
				so.planprogresslog.debug('success to forcestop plan:'+self.name)
			else:
				so.planprogresslog.debug('failed to forcestop plan:'+self.name)

	@exceptioncatchcommon
	def stop(self):
		global planhandlers
		if self.status==so.planstatus[3]:
			planhandlers.pop(self.name)
			return True
		else:
			if self.status!=so.planstatus[2]:
				for i in self.s.queue:
					self.s.cancel(i)
				self.status=so.planstatus[3]
				self.__setplanstatus(so.planstatus[3])
				planhandlers.pop(self.name)
				return True
			else:
				return False

	@exceptioncatchcommon
	def forcestop(self):
		global planhandlers
		self.stopflag=True
		if self.status==so.planstatus[1]:
			for i in self.s.queue:
				self.s.cancel(i)
		else:
			if self.status!=so.planstatus[3]:
				self.runningmanager.waitingqueue=[]
				runqueue.popqueue(self.name)
				so.runmanagerlog.info('pop self from runqueue :'+str(self.name))
				self.runningmanager.flushrunmanager()	#至少20秒
			else:
				planhandlers.pop(self.name)
				return True
		time.sleep(1)	
		self.status=so.planstatus[3]
		self.__setplanstatus(so.planstatus[3])
		planhandlers.pop(self.name)
		so.planprogresslog.info('plan '+self.name+' has been forcestopped')
		return True

	@exceptioncatchcommon
	def finishedtocall(self):
		global planhandlers
		try:
			from atplatform.plan.mappedtable import *
		except:
			pass
		if self.stopflag==True:
			self.stopflag=False
		else:
			self.plantimeinfo[2]=time.time()
			so.planprogresslog.debug('plan:'+self.name+' has finish and send result')
			res=self.__senresult()
			if os.exists(cp.exctmpdir+str(planname)):
				try:
					shutil.rmtree(cp.exctmpdir+str(planname))
				except:
					so.runmanagerlog.critical('clean tmp dir error,planname:'+str(self.name))
					raise Exception('delete tmp dir failed')
			if res==True:
				so.planprogresslog.debug('plan:'+self.name+' has send result')
			else:
				tmpfile=file(self.name+'.txt','w')
				tmpfile.write(str(self.plancases)+','+repr(self.plantimeinfo)+'|||'+'workerinfo:'+repr(self.runningmanager.workerinfo))
				tmpfile.close()
				so.planprogresslog.error('plan:'+self.name+' send result failed and has save the res to local file:'+self.name+'.txt')
			s=None
			try:
				s=so.Session()
				plantmp=s.query(Plan).filter(Plan.Name==self.name).first()
				plantmp.EndTime=long(self.plantimeinfo[2])
				s.commit()
				s.close()
			except Exception,e:
				if s!=None:
					s.close()
				so.runmanagerlog.error('error occured during call finishedtocall,planname:'+self.name+',traceback:'+traceback.format_exc())
				raise e
		self.status=so.planstatus[3]
		self.__setplanstatus(so.planstatus[3])
		planhandlers.pop(self.name)
		so.planprogresslog.info('plan:'+self.name+' has finished all cases and send result')

	@exceptioncatchcommon
	def __senresult(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=cp.mqhost))
		channel = connection.channel()
		channel.queue_declare(queue='sendresult', durable=True)
		plancasesstr=repr(self.plancases)
		tmp1=plancasesstr.find('ignore')
		tmp2=plancasesstr.find(',',tmp1+29)
		_tmp=plancasesstr[tmp1+30:tmp2]
		tmp='\''+_tmp+'\''
		plancasesstr=re.sub('(?<=ignoreProtectedModeSettings\':).*?(?=, \'Plat)',tmp,plancasesstr,count=0)
		message=self.name+'::'+'planinfo::'+plancasesstr+'|||'+str(len(self.plancases))+','+repr(self.plantimeinfo)+'|||'+'workerinfo:'+repr(self.runningmanager.workerinfo)
		channel.basic_publish(exchange='',
		                      routing_key="sendresult",
		                      body=message,
		                      properties=pika.BasicProperties(
		                         delivery_mode = 2, # make message persistent
		                      ))
		connection.close()
		return True
		
	def __setplanstatus(self,status):
		s=None
		try:
			from atplatform.plan.mappedtable import *
		except:
			pass
		try:
			s=so.Session()
			plantmp=s.query(Plan).filter(Plan.Name==self.name).first()
			if (plantmp!=None):
				plantmp.PlanStatus=s.query(PlanStatus).filter(PlanStatus.Name==status).first()
			s.commit()
			s.close()
		except Exception,e:
			if s!=None:
				s.close()
			so.planprogresslog.error('error occured during setplanstatus of plan:'+self.name+',traceback:'+traceback.format_exc())