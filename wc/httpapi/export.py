#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import urllib
from atplatform.wc import sharedobject as so
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import func
from sqlalchemy import desc
import traceback

def trace_back():  
    try:  
        return traceback.format_exc()  
    except:  
        return '' 

def getvalue(params,key,default=None):
	try:
		if params[key]!=default:
			return params[key]
		else:
			return default
	except:
		return default

class aut_search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=so.Session()
			res=None
			_id = self.get_argument("id",None)
			if _id!=None:
				given_name=s.query(AUT).filter(AUT.ID==int(_id)).one().Name
				res=s.query(AUT.ID,AUT.Name,AUT.Version).filter(AUT.ID!=int(_id),AUT.Name==given_name)
			else:
				subq=s.query(AUT.Name,func.max(AUT.LastModifyTime).label('LastModifyTime'),func.count(AUT).label('count')).group_by(AUT.Name).subquery()
				res=s.query(subq.c.count,AUT.ID,AUT.Name,AUT.Version,AUT.LastModifyTime).filter(AUT.Name==subq.c.Name,AUT.LastModifyTime==subq.c.LastModifyTime).group_by(subq.c.Name)
			returnlist=[]
			returnlist.append(int(res.count()))
			res=res.all()
			s.commit()
			if _id!=None:
				for r in res:
					returnlist.append([int(r.ID),'$$##'+r.Name,'$$##'+r.Version])
			else:
				for r in res:
					returnlist.append([int(r.count),int(r.ID),'$$##'+r.Name,'$$##'+r.Version])
			so.userlog.info('return '+str(len(res))+' auts by export')
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			print trace_back()
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()

class acut_search(tornado.web.RequestHandler):
	def post(self,argv):
		try:
			s=None
			res=None
			data=urllib.unquote(self.request.body)
			params=None
			try:
				params=dict([x.split('=') for x in data.split('&')])
			except:
				pass
			aut_ids = getvalue(params,'autid',None)
			s=so.Session()
			if aut_ids!=None:
				ids=aut_ids.split(',')
				acut_no_repeat=s.query(ACUT).join(ACUT.AUT).filter(AUT.ID.in_(ids)).group_by(ACUT.ID).subquery()
				subq=s.query(func.count(acut_no_repeat.c.ID).label('count'),acut_no_repeat.c.Name,acut_no_repeat.c.ACUTType_ID,func.max(acut_no_repeat.c.LastModifyTime).label('LastModifyTime')).group_by(acut_no_repeat.c.Name,acut_no_repeat.c.ACUTType_ID).subquery()
				acut_subq=s.query(ACUT.ID,ACUT.Name,ACUT.Version,ACUT.ACUTType_ID,ACUT.LocatorSUM,ACUT.LastModifyTime).join(ACUT.AUT).filter(AUT.ID.in_(ids)).group_by(ACUT.ID).subquery()
			else:
				subq=s.query(func.count(ACUT).label('count'),ACUT.Name,ACUT.ACUTType_ID,func.max(ACUT.LastModifyTime).label('LastModifyTime')).filter(ACUT.AUTSUM==0).group_by(ACUT.Name,ACUT.ACUTType_ID).subquery()
				acut_subq=s.query(ACUT.ID,ACUT.Name,ACUT.Version,ACUT.ACUTType_ID,ACUT.LocatorSUM,ACUT.LastModifyTime).filter(ACUT.AUTSUM==0).subquery()
			finnal_acut=s.query(acut_subq,subq.c.count,acut_subq.c.ID,acut_subq.c.Name,acut_subq.c.Version,acut_subq.c.ACUTType_ID,acut_subq.c.LocatorSUM).filter(acut_subq.c.Name==subq.c.Name,acut_subq.c.ACUTType_ID==subq.c.ACUTType_ID,acut_subq.c.LastModifyTime==subq.c.LastModifyTime).subquery()
			#res=s.query(acut_subq,subq.c.count,acut_subq.c.ID,acut_subq.c.Name,acut_subq.c.Version,acut_subq.c.ACUTType_ID,acut_subq.c.LocatorSUM,Locator).outerjoin(Locator,acut_subq.c.ID==Locator.ACUT_ID).filter(acut_subq.c.Name==subq.c.Name,acut_subq.c.ACUTType_ID==subq.c.ACUTType_ID,acut_subq.c.LastModifyTime==subq.c.LastModifyTime).order_by(desc(Locator.LastModifyTime))
			res=s.query(finnal_acut,Locator).outerjoin(Locator,finnal_acut.c.ID==Locator.ACUT_ID).order_by(desc(Locator.LastModifyTime))
			res=res.all()
			s.commit()
			reslist=[]
			reslist.append(len(res))
			rescontent={}
			for r in res:
				if rescontent.has_key(int(r.ID)):
					rescontent[int(r.ID)]['Locator'].append([int(r[-1].ID),'$$##'+r[-1].Value,'$$##'+r[-1].LocatorType.Name])
				else:
					rescontent[int(r.ID)]={'Count':int(r.count),'Name':'$$##'+r.Name,'Version':'$$##'+r.Version,'ACUTType':'$$##'+s.query(ACUTType.Name).filter(ACUTType.ID==r.ACUTType_ID).one()[0],'LocatorSUM':int(r.LocatorSUM),'Locator':[[int(r[-1].ID),'$$##'+r[-1].Value,'$$##'+r[-1].LocatorType.Name]] if r[-1]!=None else None}
			reslist.append(rescontent)
			# for r in res:
			# 	returnlist.append([int(r.count),int(r.ID),'$$##'+r.Name,'$$##'+r.Version,'$$##'+s.query(ACUTType.Name).filter(ACUTType.ID==r.ACUTType_ID).one()[0],int(r.LocatorSUM)])
			#so.userlog.info('return '+str(len(res))+' acuts by export')
			self.write(str(reslist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			print trace_back()
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()

class other_acut_search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=None
			res=None
			aut_ids = self.get_argument("autid",None)
			if aut_ids!=None and aut_ids.strip()=='':
				aut_ids=None
			acut_id = self.get_argument("acutid",None)
			if acut_id==None:
				self.write('acut not given')
				so.userlog.error('acut not given')
				return
			s=so.Session()
			acut=s.query(ACUT).filter(ACUT.ID==int(acut_id)).one()
			if aut_ids!=None:
				ids=aut_ids.split(',')
				acut_subq=s.query(ACUT.ID,ACUT.Name,ACUT.Version,ACUT.ACUTType_ID,ACUT.LocatorSUM).join(ACUT.AUT).filter(AUT.ID.in_(ids)).filter(ACUT.Name==acut.Name,ACUT.ACUTType_ID==acut.ACUTType_ID,ACUT.ID!=acut.ID).group_by(ACUT.ID).subquery()
			else:
				acut_subq=s.query(ACUT.ID,ACUT.Name,ACUT.Version,ACUT.ACUTType_ID,ACUT.LocatorSUM).filter(ACUT.AUTSUM==0).filter(ACUT.Name==acut.Name,ACUT.ACUTType_ID==acut.ACUTType_ID,ACUT.ID!=acut.ID).subquery()
			res=s.query(acut_subq.c.ID,acut_subq.c.Name,acut_subq.c.Version,acut_subq.c.ACUTType_ID,acut_subq.c.LocatorSUM,Locator).outerjoin(Locator,acut_subq.c.ID==Locator.ACUT_ID).order_by(desc(Locator.LastModifyTime))
			res=res.all()
			s.commit()
			reslist=[]
			reslist.append(len(res))
			rescontent={}
			for r in res:
				if rescontent.has_key(int(r.ID)):
					rescontent[int(r.ID)]['Locator'].append([int(r[-1].ID),'$$##'+r[-1].Value,'$$##'+r[-1].LocatorType.Name])
				else:
					rescontent[int(r.ID)]={'Name':'$$##'+r.Name,'Version':'$$##'+r.Version,'ACUTType':'$$##'+s.query(ACUTType.Name).filter(ACUTType.ID==r.ACUTType_ID).one()[0],'LocatorSUM':int(r.LocatorSUM),'Locator':[[int(r[-1].ID),'$$##'+r[-1].Value,'$$##'+r[-1].LocatorType.Name]] if r[-1]!=None else None}
			reslist.append(rescontent)		
			# for r in res:
			# 	returnlist.append([int(r.count),int(r.ID),'$$##'+r.Name,'$$##'+r.Version,'$$##'+s.query(ACUTType.Name).filter(ACUTType.ID==r.ACUTType_ID).one()[0],int(r.LocatorSUM)])
			#so.userlog.info('return '+str(len(res))+' acuts by export')
			self.write(str(reslist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			print trace_back()
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()

class helper(tornado.web.RequestHandler):
	def post(self,argv):
		self.set_header('Content-type','application/py')
		self.set_header('Content-Disposition','attachment; filename="objectmapping.py"')
		self.write(urllib.unquote(self.request.body[8:].replace('kl293cked710ime0',' ')))

class page_helper(tornado.web.RequestHandler):
	def get(self,argv):
		self.write('''
<html><head></head><body onload="loads()"><div><p id='show' style='display:none'>当出现下载框后可关闭此窗口</p></div><div><form name="hiddenform" action="/passwc/export.helper" method="post" style="display:none">
 <textarea type="text" name="content" id="hiddenvalue"></textarea>
</form></div></body>
<script type="text/javascript">
function loads(){
var openerhandle=window.opener;document.getElementById('hiddenvalue').value=openerhandle.tmp_res;hiddenform.submit();document.getElementById('show').removeAttribute('style');openerhandle.closethis();
}</script></html>''')