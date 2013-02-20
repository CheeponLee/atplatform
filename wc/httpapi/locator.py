#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import urllib
import os
import re
from atplatform.wc import sharedobject as so
from atplatform.wc import commonparam as cp
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
import traceback

def getvalue(params,key,default=None):
	try:
		if params[key]!=default:
			return params[key]
		else:
			return default
	except:
		return default

def _strip(_str):
	if _str!=None:
		return _str.strip()
	else:
		return None

class add(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict([x.split('=') for x in data.split('&')])
			value=getvalue(params,'value','')
			locatortype=getvalue(params,'type','')
			acutid=getvalue(params,'acutid','')
			DESC=getvalue(params,'DESC')
			if value=='' or locatortype.strip()=='' or acutid=='':
				self.write('failed,key params not complete')
				so.userlog.error('key params not complete')
				return
			vali_res=self.validation(acutid,value,DESC)
			if vali_res!='pass':
				return
			sess=so.Session()
			acut=sess.query(ACUT).filter(ACUT.ID==int(acutid)).one()
			_locatortype=sess.query(LocatorType).filter(LocatorType.Name==locatortype).one()
			locator=Locator(value)
			locator.ACUT=acut
			locator.LocatorType=_locatortype
			locator.DESC=DESC
			sess.add(locator)
			sess.commit()
			self.write('success,'+str(locator.ID))
			so.userlog.info('add locator success to acut:'+str(acutid)+',locatorid='+str(locator.ID))
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during add locator,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

	def validation(self,acutid,value,DESC):
		if acutid==None:
			self.write('failed,acut not given')
			so.userlog.error('acut not given')
			return 'not pass'
		if value==None or value=='':
			self.write('failed,value is null')
			so.userlog.error('value is None')
			return 'not pass'
		if len(value)>100:
			self.write('failed,value too long')
			so.userlog.error('value too long')
			return 'not pass'
		if DESC!=None and len(DESC)>200:
			self.write('failed,DESC too long')
			so.userlog.error('DESC too long')
			return 'not pass'
		return 'pass'

class modify(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict([x.split('=') for x in data.split('&')])
			_id=getvalue(params,'id')
			value=getvalue(params,'value',None)
			locatortype=getvalue(params,'type',None)
			acutid=getvalue(params,'acutid',None)
			DESC=getvalue(params,'DESC',None)
			vali_res=self.validation(_id,value,DESC)
			if vali_res!='pass':
				return
			sess=so.Session()
			locators=sess.query(Locator).filter(Locator.ID==_id).all()
			if len(locators)==0:
				so.userlog.info('locator not exist')
				self.write(failed,'locator not exist')
				return
			locator=locators[0]
			if str(value)=='' or str(locatortype).strip()=='' or str(acutid).strip()=='':
				so.userlog.error('cannot set key property empty')
				self.write('failed,cannot set key property empty')
				return
			acut=None
			if acutid!=None:
				acut=sess.query(ACUT).filter(ACUT.ID==int(acutid)).one()
			_locatortype=None
			if locatortype!=None:
				_locatortype=sess.query(LocatorType).filter(LocatorType.Name==locatortype).one()
			if value!=None:
				locator.Value=value
			if acut!=None:
				locator.ACUT=acut
			if _locatortype!=None:
				locator.LocatorType=_locatortype
			if DESC!=None:
				locator.DESC=DESC
			sess.commit()
			so.userlog.info('modify locator success')
			self.write('success')
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during modify locator,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

	def validation(self,_id,value,DESC):
		if _id==None:
			self.write('failed,locatorid is null')
			so.userlog.error('locatorid is None')
			return 'not pass'
		if value==None or value=='':
			self.write('failed,value is null')
			so.userlog.error('value is None')
			return 'not pass'
		if len(value)>100:
			self.write('failed,value too long')
			so.userlog.error('value too long')
			return 'not pass'
		if DESC!=None and len(DESC)>200:
			self.write('failed,DESC too long')
			so.userlog.error('DESC too long')
			return 'not pass'
		return 'pass'

#http://localhost:774/locator.search?value=95&type=&value_searchstyle=regexp&range=1,20
class search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=None
			_id = self.get_argument("id",None)
			if _id==None:
				value = self.get_argument("value",None)
				value_searchstyle=self.confirmsearchstyle(self.get_argument("value_searchstyle",'like'))
				locatortype= self.get_argument("type",None)
				acutidstr = self.get_argument("acutid",None)
				acutid=None
				if acutidstr!=None and acutidstr!='':
					acutid=int(acutidstr)
				#auttype = self.get_argument("auttype",None)
				DESC = self.get_argument("DESC",None)
				desc_searchstyle=self.confirmsearchstyle(self.get_argument("desc_searchstyle",'like'))
			else:
				value=None
				locatortype = None
				DESC=None
				acutid=None
			_range = self.get_argument("range",None)
			s=so.Session()
			res=s.query(Locator)
			if _id!=None:
				res=res.filter(Locator.ID==int(_id))
			returnlist=[]
			if value==None and locatortype == None and DESC==None and acutid==None:
				pass
			else:
				#import pdb;pdb.set_trace()
				if value!=None and value!='':
					res=eval('res.filter(Locator.Value.'+value_searchstyle+'(value))')
				if locatortype!=None:
					res=res.filter(Locator.LocatorType==s.query(LocatorType).filter(LocatorType.Name==locatortype).one())
				if DESC!=None and DESC!='':
					res=eval('res.filter(Locator.DESC.'+desc_searchstyle+'(DESC))')
				if acutid!=None and acutid>=0:
					res=res.filter(Locator.ACUT_ID==acutid)
			res=res.order_by(desc(Locator.LastModifyTime))
			returnlist.append(int(res.count()))
			if _range!=None:
				_range=[int(x) for x in _range.split(',')]
				res=res[_range[0]:_range[1]]
			else:
				res=res.all()
			s.commit()
			for r in res:
				returnlist.append([int(r.ID),'$$##'+r.Value,'$$##'+r.LocatorType.Name,'$$##'+r.ACUT.Name+':'+r.ACUT.Version+"("+r.ACUT.ACUTType.Name+")",int(r.Referenced),'$$##'+str(r.DESC).decode('utf8')])
			so.userlog.info('return '+str(len(res))+' locators')
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()

	def confirmsearchstyle(self,style):
		if style!='like':
			return "op('regexp')"
		else:
			return 'like'
		
class delete(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict(t.split('=') for t in [i for i in data.split('&')])
			ids=params['deleteids']
			res={}
			if ids==None or ids.strip()=='':
				self.write(failed)
				so.userlog.error('locatorid not given for deleting')
				return
			sess=so.Session()
			for x in ids.split(','):
				casenames=[]
				try:
					cases_ids=None
					distlocator=sess.query(Locator).filter(Locator.ID==int(x)).one()
					flag=True
					if len(distlocator.ACUT_Locator_Case_rel)!=0:
						cases=sess.query(ACUT_Locator_Case_rel.Case_ID).filter(ACUT_Locator_Case_rel.Locator_ID==int(x)).group_by(ACUT_Locator_Case_rel.Case_ID)
						cases_ids=[i[0] for i in cases.all()]
						flag,casenames=self.modifycasefile(int(x),distlocator.LocatorType.Name,distlocator.Value,cases_ids, sess)
					if (flag==True):
						sess.delete(distlocator)
						sess.commit()
						self.replacecasefile(casenames)
						res[x]='success'
					else:
						res[x]='failed'
				except Exception,e:
					so.userlog.error('delete locator:'+str(x)+' failed'+',traceback:'+str(traceback.format_exc()))
					res[x]='failed'
					sess.rollback()
					for casename in casenames:
						if os.path.exists(cp.cases_location+casename+'\\'+'objectmapping_replace.py') and os.path.exists(cp.cases_location+casename+'\\'+'objectmapping.py'):
							try:
								os.remove(cp.cases_location+casename+'\\'+'objectmapping_replace.py')
							except:
								so.userlog.critical('remove modifycasefile tmpfile failed, filepath:'+cp.cases_location+casename+'\\'+'objectmapping_replace.py')
								raise Exception('remove modifycasefile tmpfile failed, filepath:'+cp.cases_location+casename+'\\'+'objectmapping_replace.py')
			sess.commit()
			so.userlog.info('delete locator:'+str(res))
			self.write(str(res).replace('None','null'))
		except Exception,e:
			so.userlog.error('error occured during delete locator,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
	
	def modifycasefile(self,locatorid,locatortype,value,cases_ids,s):
		casenames=[]
		f=None
		fr=None
		try:
			for case_id in cases_ids:
				casename=s.query(Case.Name).filter(Case.ID==case_id).one()[0]
				casenames.append(casename)
				if not (os.path.exists(cp.cases_location+casename) and os.path.exists(cp.cases_location+casename+'\\'+'objectmapping.py')):
					so.userlog.error('case file not found,casename:'+str(casename)+',given path:'+str(cp.cases_location+casename+'\\'+'objectmapping.py'))
					return False,None
				f=open(cp.cases_location+casename+'\\'+'objectmapping.py','r+')
				fr=file(cp.cases_location+casename+'\\'+'objectmapping_replace.py','w+')
				line=f.readline()
				while(line!=''):
					matchedstr=re.search(r'search\(\s*driver\s*,\s*(\d+)\s*,\s*'+str(locatorid)+r'\s*\)\s*',line)
					writeline=line
					if matchedstr!=None:
						acutid=matchedstr.groups()[0]
						distacut=s.query(ACUT).filter(ACUT.ID==acutid).one()
						writeline=writeline.replace(matchedstr.group(),'we(driver,"'+str(distacut.ACUTType.Name)+'",["'+str(locatortype)+'","'+str(value)+'"])\n')
					fr.write(writeline)
					line=f.readline()
				f.close()
				fr.close()
			return True,casenames
		except Exception,e:
			so.userlog.error('error occured during modifycasefile,casename:'+str(casenames[-1])+',traceback:'+str(traceback.format_exc()))
			if f!=None:
				f.close()
			if fr!=None:
				fr.close()
			for casename in casenames:
				if os.path.exists(cp.cases_location+casename+'\\'+'objectmapping_replace.py'):
					try:
						os.remove(cp.cases_location+casename+'\\'+'objectmapping_replace.py')
					except:
						so.userlog.critical('remove modifycasefile tmpfile failed, filepath:'+cp.cases_location+casename+'\\'+'objectmapping_replace.py')
						raise Exception('remove modifycasefile tmpfile failed, filepath:'+cp.cases_location+casename+'\\'+'objectmapping_replace.py')


	def replacecasefile(self,casenames):
		for casename in casenames:
			os.remove(cp.cases_location+casename+'\\'+'objectmapping.py')
			os.rename(cp.cases_location+casename+'\\'+'objectmapping_replace.py',cp.cases_location+casename+'\\'+'objectmapping.py')