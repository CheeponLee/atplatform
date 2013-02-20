#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.ioloop
import traceback
import logging
import tornado.web
from lxml import etree
import sys
sys.path.append('/home/uls/workplace/atplatform/')
from atplatform.plan.runengine.runningmanager import *
from atplatform.plan.runengine import execute
import time
from sqlalchemy.exc import *
from atplatform.plan.runengine import runninginfo
from atplatform.plan import testlogging
reload(sys)
import thread
import urllib
from atplatform.plan.redisproccess import redisconnector as rc
import atplatform.plan.sharedobject as so
from atplatform.plan.plan import planhandlers
from sqlalchemy import desc
from sqlalchemy import func
import os
import shutil

if __name__ == "__main__":
	so.Init()
try:
	from atplatform.plan.mappedtable import *
except:
	pass
from atplatform.plan.plan import plan
from atplatform.plan.plan import planhandlers

sys.setdefaultencoding('utf8')


class excuteplan(tornado.web.RequestHandler):
	def post(self,argv):
		s=None
		planname=None
		try:
			so.planprogresslog.info('receive execute plan request')
			#读取plan schema文件
			data=urllib.unquote(self.request.body)
			a=file("schema.xsd")
			s=a.read()
			a.close()
			#生成schema对象，并提取参数
			so.planprogresslog.info('check request body xml format')
			schema_root = etree.XML(s)
			schema = etree.XMLSchema(schema_root)
			parser = etree.XMLParser(schema = schema)
			root = etree.fromstring(data, parser)
			planname=root[0].text.strip()
			so.planprogresslog.info('plan '+str(planname)+' xml format checked passed')
			if len(str(planname))>50:
				self.write('failed,planname too long')
				so.planprogresslog.error('planname too long,plan: '+str(planname))
				return
			s=so.Session()
			so.planprogresslog.debug('dbsession opened one for '+'plan '+str(planname))
			res=s.query(Plan).filter(Plan.Name==planname)
			so.planprogresslog.info('check plan '+str(planname)+' exist or not')
			if (res.count()!=0):
				s.close()
				self.write("plan already exist!")
				so.planprogresslog.error('plan '+str(planname)+' has already exist')
				return
			so.planprogresslog.info('plan '+str(planname)+' nonexistence check passed')
			starttime=root[1].text
			l=[]
			for case in root[2]:
				casename=case[0].text
				config={}
				config['Browsername']=case[1][0].text
				if case[1][1].text!=None:
					config['Browserversion']=case[1][1].text
				else:
					config['Browserversion']=''
				if case[1][2].text.startswith('t'):
					config['ignoreProtectedModeSettings']=True
				else:
					config['ignoreProtectedModeSettings']=False
				if case[1][3].text!=None:
					config['Platform']=case[1][3].text
				else:
					config['Platform']='ANY'
				config['Findtimeout']=int(case[1][4].text)
				config['Webdriverhub']=case[1][5].text
				if case[1][6].text.startswith('t'):
					config['Javascriptenabled']='True'
				else:
					config['Javascriptenabled']='False'
				l.append([casename,config])
			so.planprogresslog.debug('plan info has been extracted')
			p=plan()
			p.name=str(planname)
			re=p.setplanstarttime(starttime.strip())
			if re==False:
				s.close()
				self.write("timeset error")
				so.planprogresslog.error('plan(object) '+str(planname)+' timeset error')
				return
			so.planprogresslog.info('plan(object) '+str(planname)+' timeset success')
			p.setplancases(l)
			planhandlers[planname]=p
			plan_add=Plan(planname)
			plan_add.PlanStatus=s.query(PlanStatus).filter(PlanStatus.Name==so.planstatus[4]).first()
			plan_add.CreateTime=long(p.plantimeinfo[0])
			plan_add.StartTime=long(p.plantimeinfo[1])
			s.add(plan_add)
			check_c_p={}
			check_cp_bp={}
			casecache={}
			browsercache={}
			for _case in l:
				if not check_c_p.has_key(str([_case[0],planname])):
					rel_case=None
					if casecache.has_key(str([_case[0],planname])):
						rel_case=casecache[str([_case[0],planname])]
					else:
						rel_case=s.query(Case).filter(Case.Name==_case[0]).one()
						casecache[str([_case[0],planname])]=rel_case
					cip=Case_in_Plan()
					cip.Case=rel_case
					cip.Plan=plan_add
					s.add(cip)
					check_c_p[str([_case[0],planname])]=cip
				if not check_cp_bp.has_key((str([_case[0],planname]),str([_case[1]['Platform'],_case[1]['Browsername'],_case[1]['Browserversion']]))):
					rel_browser=None
					if browsercache.has_key(str([_case[0],planname])):
						rel_browser=casecache[str([_case[1]['Platform'],_case[1]['Browsername'],_case[1]['Browserversion']])]
					else:
						rel_browser=s.query(Browser_on_Platform).join(Browser_on_Platform.Browser).join(Browser_on_Platform.Platform).filter(Browser.Name==_case[1]['Browsername'],Browser.Version==_case[1]['Browserversion'],Platform.Name==_case[1]['Platform'],Browser_on_Platform.Browser_on_Platform_Status_ID==1).one()
						casecache[str([_case[1]['Platform'],_case[1]['Browsername'],_case[1]['Browserversion']])]=rel_case
					check_c_p[str([_case[0],planname])].Browser_on_Platform.append(rel_browser)
					check_cp_bp[(str([_case[0],planname]),str([_case[1]['Platform'],_case[1]['Browsername'],_case[1]['Browserversion']]))]=True
			s.commit()
			s.close()
			so.planprogresslog.debug('close dbsession for plan '+str(planname))
			so.planprogresslog.info('plan '+str(planname)+' has insert all info to database')
			p.run()
			so.planprogresslog.info('plan '+str(planname)+' has get in schedual')
			self.write('success!')
		except IntegrityError,e:
			so.planprogresslog.error(str(traceback.format_exc()))
			if s!=None:
				s.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.planprogresslog.error(str(traceback.format_exc()))
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()
				so.planprogresslog.debug('close dbsession for plan '+str(planname)+' as error occured')
#plan1::planinfo:planrawinfostr,2,[1347505606.092, 1347505611.092, 1347505637.824]|||workerinfo:{'case2__2012-09-13__Thursday__11.06.51__\xe4\xb8\xad\xe5\x9b\xbd\xe6\xa0\x87\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4': ['stopped', 1347505612.917, 1347505628.089, 'success', '', ''], 'case2__2012-09-13__Thursday__11.06.53__\xe4\xb8\xad\xe5\x9b\xbd\xe6\xa0\x87\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4': ['stopped', 1347505622.95, 1347505637.824, 'success', '', '']}

#只能从内存中查找plan进度
class checkplanprogress(tornado.web.RequestHandler):
	def get(self,argv):
		planname=None
		try:
			planname=self.get_argument('planname')
			so.userlog.info('received planstatus of '+str(planname)+' check request')
			if planname==None:
				so.userlog.error('planname is null')
				self.write('planname is null')
				return
			if planname in planhandlers.keys():
				try:
					planstatus=planhandlers[planname].checkstatus()
					if planstatus!=False:
						self.write(planstatus[0]+','+str(planstatus[1][0])+','+str(planstatus[1][1]))
						so.userlog.info('checkplanprogress success,planname:'+str(planname)+',result:'+str(planstatus))
					else:
						self.write('failed')
						so.userlog.error(planname+":"+"error ocurred during checkplanprogress,see previous log for detailed infomation")
				except Exception,e:
					self.write(planname+":"+"error ocurred , "+str(e))
					so.userlog.error(planname+":"+"error ocurred , "+str(traceback.format_exc()))
			else:
				self.write(planname+":The plan does not in the memory")
				so.userlog.error('check failed,'+planname+" not in the memory")
		except Exception,e:
			so.userlog.error('planstatus of '+str(planname)+' check failed,'+str(traceback.format_exc()))
			self.write("failed")

class planinfo(tornado.web.RequestHandler):
	def get(self,argv):
		planname=None
		try:
			planname=self.get_argument('planname')
			so.userlog.info('received getting '+str(planname)+' planinfo request')
			if planname in planhandlers.keys() and planhandlers[planname].status!=so.planstatus[0]:
				try:
					plan=planhandlers[planname]
					plantimeinfo=plan.plantimeinfo
					if plantimeinfo[2]!=None and plantimeinfo[2]!=0:
						self.write('planname:'+str(planname)+',plancases:'+str(len(plan.plancases))+',plancreatedtime:'+time.ctime(plantimeinfo[0])+',planstartexcutetime:'+time.ctime(plantimeinfo[1])+',planendexcutetime:'+time.ctime(plantimeinfo[2]))
						so.userlog.info('planname: get '+str(planname)+' planinfo success')
					else:
						self.write('planname:'+str(planname)+',plancases:'+str(len(plan.plancases))+',plancreatedtime:'+time.ctime(plantimeinfo[0])+',planstartexcutetime:'+time.ctime(plantimeinfo[1])+',planendexcutetime:unkown')
						so.userlog.info('planname: get '+str(planname)+' planinfo success')
				except Exception,e:
					self.write(planname+":"+"error ocurred , "+str(e))
					so.userlog.error('get '+str(planname)+' planinfo failed,'+str(traceback.format_exc()))
			else:
				self.write(str(planname)+":The plan does not exist or not planned")
				so.userlog.error('planstatus check failed as the plan not exist or not planned')
		except:
			self.write('failed')
			so.userlog.error('error occured during get '+str(planname)+' planinfo,'+str(traceback.format_exc()))

class stopplans(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			so.userlog.info('received stoplans request')
			planlist={}
			plannames=eval(self.get_argument('plannames'))
			for planname in plannames:
				res=stopplan._do(planname)
				if (res.find('success')>=0):
					planlist[planname]='success'
					so.userlog.info('plan '+str(planname)+' stop success')
				else:
					if (res.find('this plan has started to run')>=0):
						so.userlog.info('plan '+str(planname)+' has started to run,try forcestop')
						res2=forcestopplan._do(planname)
						if (res2.find('success')>=0):
							planlist[planname]='success'
							so.userlog.info('plan '+str(planname)+' forcestop success')
						else:
							planlist[planname]='failed'
							so.userlog.info('plan '+str(planname)+' forcestop failed')
					else:
						planlist[planname]='failed'
						so.userlog.info('plan '+str(planname)+' stop failed')
			self.write(str(planlist).replace('None','null'))
		except Exception,e:
			self.write('stop plans failed')
			so.userlog.error('stop plans failed,error occured,'+str(traceback.format_exc()))
			

class stopplan(tornado.web.RequestHandler):
	def get(self,argv):
		planname=None
		planname=self.get_argument('planname')
		try:
			so.userlog.info('received stoplan '+planname+' request')
			res=self._do(self,planname)
			self.write(res)
			so.userlog.info('stop plan '+str(planname)+' res:'+str(res))
		except:
			so.userlog.error('stop plan '+str(planname)+' failed,error occured,'+str(traceback.format_exc()))
			self.write('failed')

	@classmethod
	def _do(self,planname):
		so.userlog.info('start stop plan:'+str(planname))
		s=None
		try:
			if planname in planhandlers.keys():
				so.userlog.debug('begin stop the plan:'+str(planname))
				res=planhandlers[planname].stop()
				so.userlog.debug('stop signal has send to the plan:'+str(planname))
				if res==True:
					so.userlog.debug('stop plan'+str(planname)+' success,begin write this to db')
					s=so.Session()
					s.delete(s.query(Plan).filter(Plan.Name==planname).first())
					s.commit()
					s.close()
					so.userlog.info('plan '+str(planname)+' has stopped and removed from db')
					return str(planname)+": success"
				else:
					so.userlog.info('plan '+str(planname)+' stop failed,this plan has started to run')
					return str(planname)+": this plan has started to run"
			else:
				so.userlog.debug('plan '+str(planname)+' not in memory,start check it in db')
				s=so.Session()
				so.userlog.debug('open one db session for stop plan '+str(planname))
				r=s.query(Plan).filter(Plan.Name==planname).first()
				if (r!=None):
					s.delete(r)
					s.commit()
					s.close()
					so.userlog.info('plan '+str(planname)+' stop success,(direct remove from db)')
					return str(planname)+": success"
				else:
					s.close()
					so.userlog.debug('close db session for stop plan '+str(planname))
					so.userlog.info('stop plan '+str(planname)+' success')
					return str(planname)+":The plan does not exist!"
			if os.path.exists(os.path.join(cp.exctmpdir,planname)):
				shutil.rmtree(os.path.join(cp.exctmpdir,planname))
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('stop plan '+str(planname)+' failed,error occured,'+str(traceback.format_exc()))
			return str(planname)+":"+"error ocurred , "+str(e)

class forcestopplan(tornado.web.RequestHandler):
	def get(self,argv):
		planname=None
		planname=self.get_argument('planname')
		try:
			so.userlog.info('received forcestop plan '+planname+' request')
			res=self._do(planname)
			self.write(res)
			so.userlog.info('stop plan '+str(planname)+' res:'+str(res))
		except:
			so.userlog.error('forcestop plan '+str(planname)+' failed,error occured,'+str(traceback.format_exc()))
			self.write('failed')

	@classmethod
	def _do(self,planname):
		s=None
		try:
			so.userlog.debug('check plan '+str(planname)+' existence')
			if planname in planhandlers.keys():
				so.userlog.debug('plan '+str(planname)+' exist')
				so.userlog.debug('plan '+str(planname)+' start to forcestop')
				res=planhandlers[planname].forcestop()
				if res==True:
					so.userlog.debug('plan '+str(planname)+' forcestop success and ready to write it to db')
					s=so.Session()
					so.userlog.debug('open a db session for forcestop plan:'+str(planname))
					s.delete(s.query(Plan).filter(Plan.Name==planname).first())
					s.commit()
					s.close()
					so.userlog.debug('close db session for forcestop plan:'+str(planname))
					so.userlog.info('forcestop plan '+str(planname)+ ' success')
					return planname+": success"
				else:
					so.error('forcestop plan '+str(planname)+ ' failed')
					return planname+": stop failed"
			else:
				so.userlog.debug('open a db session for forcestop plan:'+str(planname))
				s=so.Session()
				r=s.query(Plan).filter(Plan.Name==planname).first()
				if (r!=None):
					so.userlog.debug('plan '+str(planname)+' in db,start deleting it from db')
					s.delete(r)
					s.commit()
					s.close()
					so.userlog.info('remove plan '+str(planname)+' direct from db')
					return planname+": success"
				else:
					s.close()
					so.userlog.debug('close db session for forcestop plan:'+str(planname))
					so.error('plan '+str(planname)+' not exist')
					return planname+":The plan does not exist!"
			if os.path.exists(os.path.join(cp.exctmpdir,planname)):
				shutil.rmtree(os.path.join(cp.exctmpdir,planname))
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('forcestop plan '+str(planname)+' failed,error occured,'+str(traceback.format_exc()))
			return planname+":"+"error ocurred , "+str(e)

class getcases(tornado.web.RequestHandler):
	def get(self,argv):
		status=None
		s=None
		try:
			status=self.get_argument('status',None)
			so.userlog.info('received getcases('+str(status)+') request')
			s=so.Session()
			so.userlog.debug('open a session for getcases('+str(status)+')')
			if (status==None):
				rs=s.query(Case)
			else:
				if status[0:1]=='!':
					rs=s.query(Case).join(Case.CaseStatus).filter(CaseStatus.Name!=status[1:])
				else:
					rs=s.query(Case).filter(Case.CaseStatus==status)
			caselist=[]
			for r in rs:
				caselist.append('$$##'+r.Name)
			s.close()
			so.userlog.debug('close session for getcases('+str(status)+')')
			self.write(str(caselist).replace('None','null').replace("u'$$##","'"))
			so.userlog.info('getcases('+str(status)+') request success,return reslist')
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('getcases('+str(status)+') failed,error occured,'+str(traceback.format_exc()))

class getplans(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		planname=None
		try:
			planname = self.get_argument("planname",None)
			displayrange = self.get_argument("range",'all')
			so.userlog.info('received getplans request, planname:'+str(planname)+' range:'+str(displayrange))
			so.userlog.debug('open a session for getplans planname:'+str(planname)+' range:'+str(displayrange))
			s=so.Session()
			planlist=[]
			rs=[]
			if planname==None:
				allres=s.query(Plan,Report).outerjoin(Plan.Report).order_by(desc(func.ifnull(Plan.LastModifyTime,0)))
				if displayrange=='all':
					rs=allres
				else:
					displayrange=eval(displayrange)
					rs=allres[displayrange[0]:displayrange[1]]
				planlist.append(str(allres.count()))
				for r in rs:
					planprogress=self.getplanstatus(r[0].Name)
					print "planprogress:"+str(planprogress)
					planlist.append(['$$##'+r[0].Name,'$$##'+r[0].PlanStatus.Name,None if r[0].CreateTime==None else u'$$##'+str(r[0].CreateTime),None if r[0].StartTime==None else u'$$##'+str(r[0].StartTime),None if r[0].EndTime==None else u'$$##'+str(r[0].EndTime),None if r[0].DESC==None else '$$##'+str(r[0].DESC).decode('utf8'),None if r[1]==None else ['$$##'+r[1].Name,'$$##'+r[1].ReportStatus.Name],planprogress])
			else:
				allres=s.query(Plan,Report).outerjoin(Plan.Report).filter(Plan.Name.like(planname+"%")).order_by(desc(func.ifnull(Plan.LastModifyTime,0)))
				if displayrange=='all':
					rs=allres
				else:
					displayrange=eval(displayrange)
					rs=allres[displayrange[0]:displayrange[1]]
				planlist.append(str(allres.count()))
				for r in rs:
					planprogress=self.getplanstatus(r[0].Name)
					print "planprogress:"+str(planprogress)
					planlist.append(['$$##'+r[0].Name,'$$##'+r[0].PlanStatus.Name,None if r[0].CreateTime==None else u'$$##'+str(r[0].CreateTime),None if r[0].StartTime==None else u'$$##'+str(r[0].StartTime),None if r[0].EndTime==None else u'$$##'+str(r[0].EndTime),None if r[0].DESC==None else '$$##'+str(r[0].DESC).decode('utf8'),None if r[1]==None else ['$$##'+r[1].Name,'$$##'+r[1].ReportStatus.Name],planprogress])
			s.close()
			so.userlog.debug('close session for getplans planname:'+str(planname)+' range:'+str(displayrange))
			self.write(str(planlist).replace('None','null').replace("u'$$##","'"))
			so.userlog.info('getplans request process success, planname:'+str(planname)+' range:'+str(displayrange))
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('getplans failed,error occured,'+str(traceback.format_exc()))

	def getplanstatus(self,planname):
		planprogress=None
		try:
			if planhandlers[planname]!=None:
				status_res=planhandlers[planname].checkstatus()
				if status_res!=False:
					planprogress=status_res[1]
			return planprogress
		except:
			return planprogress

class checkplanexist(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		planname=None
		try:
			planname = self.get_argument("planname",None)
			so.userlog.info('received checkplanexist request, planname:'+str(planname))
			s=so.Session()
			so.userlog.debug('open a session for checkplanexist planname:'+str(planname))
			if planname!=None and str(planname).strip()!="":
				rs=s.query(Plan).filter(Plan.Name==planname)
				if rs.count()!=0:
					info=u"plan exist"
				else:
					info=u"plan not exist"
			else:
				info=u"planname is null"
			s.close()
			so.userlog.debug('close session for checkplanexist planname:'+str(planname))
			self.write(str(info).replace('None','null').replace("u'","'"))
			so.userlog.info('checkplanexist request process success,planname:'+str(planname))
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('process checkplanexist request failed,planname:'+str(planname)+',error occured,'+str(traceback.format_exc()))

class getplatforms(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		try:
			so.userlog.info('received getplatforms request')
			s=so.Session()
			so.userlog.debug('open a session for getplatforms')
			rs=s.query(Platform)
			platformlist=[]
			for r in rs:
				platformlist.append('$$##'+r.Name)
			s.close()
			so.userlog.debug('close session for getplatforms')
			self.write(str(platformlist).replace('None','null').replace("u'$$##","'"))
			so.userlog.info('getplatforms request process success')
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('process getplatforms request failed,error occured,'+str(traceback.format_exc()))

class getbrowsers(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		platform=None
		try:
			platform = self.get_argument("platform",None)
			so.userlog.info('received getbrowsers('+str(platform)+') request')
			s=so.Session()
			so.userlog.debug('open a session for getbrowsers('+str(platform)+')')
			browsers=[]
			if platform==None:
				rs=s.query(Browser)
				for r in rs:
					browsers.append(['$$##'+r.Name,'$$##'+r.Version])
			else:
				rs=s.query(Browser_on_Platform).join(Browser_on_Platform.Platform).filter(Platform.Name==platform,Browser_on_Platform.Browser_on_Platform_Status_ID==1)
				for r in rs:
					browsers.append(['$$##'+r.Browser.Name,'$$##'+r.Browser.Version])
			s.close()
			so.userlog.debug('close session for getbrowsers('+str(platform)+')')
			self.write(str(browsers).replace('None','null').replace("u'$$##","'"))
			so.userlog.info('getbrowsers('+str(platform)+') request process success')
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('process getbrowsers('+str(platform)+') request failed,error occured,'+str(traceback.format_exc()))

class checksamenamereport(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		planname=None
		try:
			planname = self.get_argument("planname",None)
			so.userlog.info('received checksamenamereport('+str(planname)+') request')
			if planname==None:
				self.write('failed,planname is null')
				return
			s=so.Session()
			so.userlog.debug('open a session for checksamenamereport('+str(planname)+')')
			res=s.query(Report).filter(Report.Name==str(planname))
			reslength=res.count()
			s.close()
			so.userlog.debug('close session for checksamenamereport('+str(planname)+')')
			if reslength==0:
				self.write('success,passed')
			else:
				self.write('success,unpassed')
			so.userlog.info('checksamenamereport('+str(planname)+') request process success')
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			so.userlog.error('process checksamenamereport('+str(planname)+') request failed,error occured,'+str(traceback.format_exc()))

class deletesamenamereport(tornado.web.RequestHandler):
	def get(self,argv):
		s=None
		reportname=None
		try:
			reportname = self.get_argument("reportname",None)
			so.userlog.info('received deletesamenamereport('+str(reportname)+') request')
			if reportname==None:
				self.write('failed,reportname is null')
				return
			s=so.Session()
			so.userlog.debug('open a session for deletesamenamereport('+str(reportname)+')')
			report=s.query(Report).filter(Report.Name==str(reportname)).one()
			s.delete(report)
			s.commit()
			s.close()
			so.userlog.debug('close session for deletesamenamereport('+str(reportname)+')')
			self.write('success')
			so.userlog.info('deletesamenamereport('+str(reportname)+') request process success')
		except Exception,e:
			if s!=None:
				s.rollback()
				s.close()
			self.write('failed')
			so.userlog.error('process deletesamenamereport('+str(reportname)+') request failed,error occured,'+str(traceback.format_exc()))

class StaticWWWHandler(tornado.web.StaticFileHandler):
	pass

urls = [
	('/www/(.*)',StaticWWWHandler,dict(path=cp.home+'static/')),
	('/excuteplan(.*)', excuteplan),
	('/checkplanprogress(.*)',checkplanprogress),
	('/stopplans(.*)',stopplans),
	('/stopplan(.*)',stopplan),
	('/forcestopplan(.*)',forcestopplan),
	('/planinfo(.*)',planinfo),
	('/getcases(.*)',getcases),
	('/getplans(.*)',getplans),
	('/checkplanexist(.*)',checkplanexist),
	('/getplatforms(.*)',getplatforms),
	('/getbrowsers(.*)',getbrowsers),
	('/checksamenamereport(.*)',checksamenamereport),
	('/deletesamenamereport(.*)',deletesamenamereport)
]

# def joinplan(p):
# 	time.sleep(30)

if __name__ == "__main__":
	s=None
	try:
		testlogging.init(logging.DEBUG)
		so.adminlog.info('open a db session for check the plans of unstopped status')
		s=so.Session()
		res=s.query(PlanStatus).filter(PlanStatus.Name!=so.planstatus[3])
		for re in res:
			for i in re.Plan:
				s.delete(i)
		so.adminlog.info('plans of unstopped status has been delete from db')
		s.commit()
		s.close()
		so.adminlog.info('close db session')
		thread.start_new_thread(runqueue.execute,())
		application = tornado.web.Application(urls, globals())
		port=775
		so.adminlog.info('gonna setting listening port:'+str(port))
		application.listen(port)
		so.adminlog.info('server started')
		tornado.ioloop.IOLoop.instance().start()
	except Exception,e:
		if s!=None:
			s.rollback()
			s.close()
		print traceback.format_exc()
		so.adminlog.critical('server start failed,error ocurred:',str(traceback.format_exc()))
