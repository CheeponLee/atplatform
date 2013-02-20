#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import threading
import time 
import atplatform.plan.commonparam as cp
import random
from atplatform.plan.runengine import execute
import thread
import atplatform.plan.sharedobject as so
import traceback

class runqueue:
	globallock=threading.RLock()
	queue={}
	runningqueuelength=0
	#{'planname':[priority value,[(name,runmanagerinstance_self,casename,config,q),(name,runmanagerinstance_self,casename,config,q)]]}
	@staticmethod
	def push(_dict,runmanagerinstance):
		#_dict=['planname',(name,runmanagerinstance_self,casename.config.q)]
		if runmanagerinstance.stopflag!=True:
			runqueue.globallock.acquire()
			if _dict[0] in runqueue.queue.keys():
				runqueue.queue[_dict[0]][1].append(_dict[1])
			else:
				runqueue.queue[_dict[0]]=[cp.defaultweight,[_dict[1]]]
			runqueue.globallock.release()

	@staticmethod
	def execute():
		while True:
			time.sleep(10)
			#print "runqueue.runningqueuelength:::"+str(runqueue.runningqueuelength)
			runqueue.globallock.acquire()
			if len(runqueue.queue.keys())!=0 and runqueue.runningqueuelength<cp.maxconcurrent:
				#从queue中取出maxconcurrent个任务去执行
				for t in range(cp.maxconcurrent-runqueue.runningqueuelength):
					if len(runqueue.queue.keys())==0:
						break
					#prioritysum=0
					prioritysumstr=[]
					prioritylist=[]
					for i in runqueue.queue:
						prioritylist.append(i)
						#prioritysum=runqueue.queue[i][0]+prioritysum
						prioritysumstr.extend([len(prioritylist)]*runqueue.queue[i][0])
					priority=random.choice(prioritysumstr)
					executeplan=prioritylist[priority-1]
					executecaseinfo=runqueue.queue[executeplan][1].pop(0)	#取出选定的计划中的第一个case
					if len(runqueue.queue[executeplan][1])==0:
						runqueue.queue.pop(executeplan)		#如果10秒内没有新的case推送到runqueue中，则此plan在runqueue中删除
					runqueue.newworker(executecaseinfo[1],executecaseinfo[2],executecaseinfo[3],executecaseinfo[0],executecaseinfo[4],executecaseinfo[5])
					so.runmanagerlog.info('push to runqueue to excute,plan:'+str(executecaseinfo[1].planhandler.name)+',case:'+str(executecaseinfo[0]))
					runqueue.runningqueuelength=runqueue.runningqueuelength+1
					so.runmanagerlog.info('runningqueuelength +1,length:'+str(runqueue.runningqueuelength)+' from plan:'+str(executecaseinfo[1].planhandler.name))
					#runqueue.queue.pop(executeplan)
			runqueue.globallock.release()

	@staticmethod
	def newworker(runmanagerinstance,casename,config,name,q,dataq):
		p=execute.run(casename,config,name,q,dataq,planname=runmanagerinstance.planhandler.name)
		runmanagerinstance.runningworker[name]=p
		thread.start_new_thread(runmanagerinstance.__jointhread__,(name,p,q,dataq))		#开新线程__jointhread__监视worker执行结束，并执行动作
		runmanagerinstance.workerinfo[name]=[so.workerstatus[1],time.time(),'','','','',{}]
		runmanagerinstance.pushqueuecount=runmanagerinstance.pushqueuecount+1
		so.runmanagerlog.info('pushqueuecount +1,length:'+str(runmanagerinstance.pushqueuecount)+',plan:'+str(runmanagerinstance.planhandler.name))


	@staticmethod
	def popqueue(planname):
		try:
			runqueue.globallock.acquire()
			runqueue.queue.pop(planname)
			runqueue.globallock.release()
			return True
		except Exception,e:
			so.runmanagerlog.error('popqueue failed plan:'+str(planname)+',traceback:'+str(traceback.format_exc()))
			return False

	@staticmethod
	def clearqueue(planname):
		runqueue.globallock.acquire()
		runqueue.queue.clear()
		runqueue.globallock.release()
