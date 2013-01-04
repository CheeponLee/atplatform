#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import os
import urllib
import re
from atplatform.wc import sharedobject as so
from atplatform.wc import commonparam as cp
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
import traceback

def getvalue(params,key,default=None):
	try:
		if params[key]!='':
			return params[key]
		else:
			return default
	except:
		return default

class add(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict([x.split('=') for x in data.split('&')])
			name=getvalue(params,'name')
			version=getvalue(params,'version','1.0')
			acuttype=getvalue(params,'type','web_element')
			autid=getvalue(params,'autid')
			DESC=getvalue(params,'DESC')
			if name==None:
				so.userlog.error('acutname is None')
				self.write('failed,name is null')
				return
			sess=so.Session()
			newacut=ACUT(name)
			newacut.Version=version
			newacut.DESC=DESC
			newacut.ACUTType=sess.query(ACUTType).filter(ACUTType.Name==acuttype).one()
			if (autid!=None):
				autlist=[]
				for x in autid.split(','):
					autlist.append(sess.query(AUT).filter(AUT.ID==x).one())
				newacut.AUT=autlist
			sess.add(newacut)
			sess.commit()
			so.userlog.info('add acut success,acutid='+str(newacut.ID))
			self.write('success,'+str(newacut.ID))
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during add acut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

class modify(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict([x.split('=') for x in data.split('&')])
			_id=getvalue(params,'id')
			if _id==None:
				so.userlog.error('id is not given')
				self.write("failed,id is not given")
			name=getvalue(params,'name')
			version=getvalue(params,'version')
			DESC=getvalue(params,'DESC')
			acuttype=getvalue(params,'type')
			addaut=getvalue(params,'addaut')
			deleteaut=getvalue(params,'deleteaut')
			sess=so.Session()
			acuts=sess.query(ACUT).filter(ACUT.ID==_id).all()
			if len(acuts)==0:
				so.userlog.info('acut not exist')
				self.write('failed,acut not exist')
			acut=acuts[0]
			if name=='' or version=='' or acuttype=='':
				so.userlog.error('cannot set key property empty')
				self.write('failed,cannot set key property empty')
			if name!=None:
				acut.Name=name
			if version!=None:
				acut.Version=version
			if acuttype!=None:
				acut.ACUTType=sess.query(ACUTType).filter(ACUTType.Name==acuttype).one()
			if DESC!=None:
				acut.DESC=DESC
			if addaut!=None:
				for x in addaut.split(','):
					acut.AUT.append(sess.query(AUT).filter(AUT.ID==int(x)).one())
			if deleteaut!=None:
				for x in deleteaut.split(','):
					acut.AUT.remove(sess.query(AUT).filter(AUT.ID==int(x)).one())
			sess.commit()
			so.userlog.info('modify acut success')
			self.write('success')
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during modify acut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

class search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=None
			_id = self.get_argument("id",None)
			if _id==None:
				name = self.get_argument("name",None)
				name_searchstyle=self.confirmsearchstyle(self.get_argument("name_searchstyle",'like'))
				version = self.get_argument("version",None)
				version_searchstyle=self.confirmsearchstyle(self.get_argument("version_searchstyle",'like'))
				acuttype = self.get_argument("type",None)
				preautsum = self.get_argument("preautsum",-1)
				postautsum = self.get_argument("postautsum",None)
				DESC = self.get_argument("DESC",None)
				desc_searchstyle=self.confirmsearchstyle(self.get_argument("desc_searchstyle",'like'))
			else:
				name=None
				version=None
				preautsum=-1
				postautsum=None
				DESC=None
				acuttype=None
			_range = self.get_argument("range",None)
			s=so.Session()
			res=s.query(ACUT)
			if _id!=None:
				res=res.filter(ACUT.ID==int(_id))
			returnlist=[]
			if name==None and version == None and preautsum == -1 and postautsum==None and DESC==None and acuttype==None:
				pass
			else:
				if name!=None and name!='':
					res=eval('res.filter(ACUT.Name.'+name_searchstyle+'(name))')
				if version!=None and version!='':
					res=eval('res.filter(ACUT.Version.'+version_searchstyle+'(version))')
				if acuttype!=None and acuttype!='':
					res=res.filter(ACUT.ACUTType==s.query(ACUTType).filter(ACUTType.Name==acuttype).one())
				if postautsum!=None:
					res=res.filter(ACUT.AUTSUM>=preautsum,ACUT.AUTSUM<=postautsum)
				else:
					res=res.filter(ACUT.AUTSUM>=preautsum)
				if DESC!=None and DESC!='':
					res=eval('res.filter(ACUT.DESC.'+desc_searchstyle+'(DESC))')
			res=res.order_by(desc(ACUT.LastModifyTime))
			returnlist.append(int(res.count()))
			if _range!=None:
				_range=[int(x) for x in _range.split(',')]
				res=res[_range[0]:_range[1]]
			else:
				res=res.all()
			s.commit()
			for r in res:
				returnlist.append([int(r.ID),'$$##'+r.Name,'$$##'+r.Version,'$$##'+r.ACUTType.Name,int(r.LocatorSUM),int(r.AUTSUM),'$$##'+str(r.DESC).decode('utf8')])
			so.userlog.info('return '+str(len(res))+' acuts')
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error('error occured during search acut,traceback:'+str(traceback.format_exc()))
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
			sess=so.Session()
			for x in ids.split(','):
				casenames=[]
				try:
					cases_ids=None
					distacut=sess.query(ACUT).filter(ACUT.ID==int(x)).one()
					flag=True
					if len(distacut.ACUT_Locator_Case_rel)!=0:
						cases=sess.query(ACUT_Locator_Case_rel.Case_ID).filter(ACUT_Locator_Case_rel.ACUT_ID==int(x)).group_by(ACUT_Locator_Case_rel.Case_ID)
						cases_ids=[i[0] for i in cases.all()]
						flag,casenames=self.modifycasefile(int(x),distacut.ACUTType.Name,cases_ids, sess)
					if (flag==True):
						sess.delete(distacut)
						sess.commit()
						res[x]='success'
						self.replacecasefile(casenames)
					else:
						res[x]='failed'
				except Exception,e:
					so.userlog.error('delete acut:'+str(x)+' failed'+',traceback:'+str(traceback.format_exc()))
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
			so.userlog.info('delete acut:'+str(res))
			self.write(str(res).replace('None','null'))
		except Exception,e:
			so.userlog.error('error occured during delete acut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
	
	def modifycasefile(self,acutid,acuttype,cases_ids,s):
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
					matchedstr=re.search(r'search\(\s*driver\s*,\s*'+str(acutid)+r'\s*,\s*(\d+)\s*\)\s*',line)
					writeline=line
					print "matchedstr:"+str(matchedstr)
					if matchedstr!=None:
						locatorid=matchedstr.groups()[0]
						distlocator=s.query(Locator).filter(Locator.ID==locatorid).one()
						writeline=writeline.replace(matchedstr.group(),'we(driver,"'+str(acuttype)+'",["'+str(distlocator.LocatorType.Name)+'","'+str(distlocator.Value)+'"])\n')
						print "writeline:"+writeline
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