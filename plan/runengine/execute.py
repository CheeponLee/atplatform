#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from multiprocessing import Process,Queue
from atplatform.plan.runengine.exceptioncatch import *
from atplatform.plan.commonparam import *
import time
import atplatform.plan.sharedobject as so
import os
import random
import shutil
#import runningmanager as rm


#run('case1',{'Browsername':'firefox','Browserversion':'10.0','Platform':'WINDOWS','Findtimeout':30,'Webdriverhub':'http://localhost:8888/wd/hub','Javascriptenabled':'True'})
def run(casename,config,name,queue,planname=None):
	th=Process(target=exec_case, args=(casename,config,name,queue,planname))
	th.daemon=True
	th.start()
	so.runmanagerlog.info('start a process for excute:'+str(name))
	return th
	#exec_case(casename,config)

@exceptioncatch
def exec_case(casename,config,name,queue,planname=None):
	os.setuid(restricteduserid)
	distdir=exctmpdir+str(planname)+'/'+str(casename)+'_'+str(int(time.time()))+str(random.randint(1,1000))
	shutil.copytree(home+'cases/'+casename,distdir,ignore=shutil.ignore_patterns(str(casename)+'.py*','objectmapping.py*'))
	os.chdir(exctmpdir+str(planname)+'/'+str(casename))
	case=get_case(casename,config,queue)
	case.init()
	try:
		case.before()
		case.action()
	except Exception,e:
		pic=exceptionpicdir+name+'_errortime_'+time.ctime().replace(':','.')+u'.png'
		try:
			flag=case.driver.get_screenshot_as_file(pic)
		except Exception,e1:
			if (e1.msg.find('HtmlUnitDriver')<0)==False:
				flag=True
				pic='HtmlUnitDriver cannot get pic'
			else:
				raise Exception(str(e1),'')
		if flag==False:
			raise Exception(str(e)+'\n\nGenerate exceptionpic failed!','')
		raise Exception(str(e),pic)
	finally:
		case.clean()
		if os.path.exists(distdir):
			shutil.rmtree(distdir)

def get_case(casename,config,queue):
	exec('from atplatform.plan.cases.'+casename+ ' import '+casename)
	return eval(casename+'.testcase(config,queue)')
