#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

import os
import shutil
import traceback
from atplatform.report import commonparam as cp
from atplatform.report import sharedobject as so
from atplatform.report.mappedtable import *

class planresult(object):
	"""docstring for planresult"""
	def __init__(self, info):
		# try:
		super(planresult, self).__init__()
		try:
			temp1=info.find('::planinfo')
			self.planname=info[:temp1]
			temp1=info.find('planinfo::')
			temp2=info.find('|||')
			self.plancases=info[temp1+10:temp2]
			temp1=info.find(',',temp2)
			self.sumofcases=info[temp2+3:temp1]
			temp2=info.find('|||',temp1+1)
			timeinfo=eval(info[temp1+1:temp2])
			self.planedtime=str(timeinfo[0])
			self.planstarttime=str(timeinfo[1])
			self.planendtime=str(timeinfo[2])
			temp1=info.find('workerinfo:',temp2+3)
			self.casesresults=info[temp1+11:].replace(repr(cp.exceptionpiclocation)[1:-1],'').replace('u\'','\'')
		except Exception,e:
			so.processlog.error('error occured during init planresult object,traceback:'+traceback.format_exc())
			self.valid=False
		self.valid=True


	def generatereport(self):
		path=cp.resultslocation+str(self.planname)
		try:
			if os.path.exists(cp.resultstmplocation+self.planname):
				os.remove(cp.resultstmplocation+self.planname)
			filetemp=file(cp.resultstmplocation+self.planname,'w')
			filetemp.write('planname=\"'+self.planname+'\";sumofcases='+self.sumofcases+';planedtime='+self.planedtime+';planstarttime='+self.planstarttime+';planendtime='+self.planendtime+';')
			filetemp.write('cases='+self.casesresults+';')
			filetemp.write('plancases='+self.plancases+';')
			filetemp.close()
			if os.path.exists(path):
				shutil.rmtree(path)
			shutil.copytree(cp.basereportlocation,path)
			shutil.copyfile(cp.resultstmplocation+self.planname,path+'/data.js')
			os.remove(cp.resultstmplocation+self.planname)
		except Exception,e:
			so.processlog.error('error occured during generating report,traceback:'+traceback.format_exc())
			if os.path.exists(path):
				shutil.rmtree(path)
			if os.path.exists(cp.resultstmplocation+self.planname):
				os.remove(cp.resultstmplocation+self.planname)
			raise Exception(traceback.format_exc())

		
#message=self.name+'::'+'planinfo::'+repr(self.plancases)+'|||'+str(len(self.plancases))+','+repr(self.plantimeinfo)+'|||'+'workerinfo:'+repr(self.runningmanager.workerinfo)
