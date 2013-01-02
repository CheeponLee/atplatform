#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from atplatform.plan.runengine.runningmanager import *
from atplatform.plan.runengine import execute
import gc
import time
from atplatform.plan.runengine import runninginfo
from atplatform.plan.plan import plan
import sys
reload(sys)
sys.setdefaultencoding('utf8')
if __name__=='__main__':
	for x in xrange(1,2):
		p=plan()
		l=[]
		l.append(('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'}))
		l.append(('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'}))
		l.append(('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'}))
		l.append(('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'}))
		print l
		p.setplancases(l)
		p.run()
		time.sleep(20)
		p.forcestop()
		# rm=runningmanager()
		# for i in range(1):
		# 	name=rm.newworker('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':10,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'})
		# 	#rm.newworker('case1',{'Browsername':'firefox','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':30,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'})
		# 	print 'started!!!'
		# #rm.newworker('case1',{'Browsername':'chrome','ignoreProtectedModeSettings':True,'Browserversion':'','Platform':'WINDOWS','Findtimeout':30,'Webdriverhub':'http://localhost:4444/wd/hub','Javascriptenabled':'True'})
		# time.sleep(15)
		# print rm.workerinfo[name]
		# # for i in rm.workerinfo[name]:
		# # 	for t in i[1:]:
		# # 		print t
		time.sleep(80)

	# thread.start_new_thread(ex,(re,testcase1('Chrome')))
	
