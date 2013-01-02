#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import urllib
from atplatform.wc import sharedobject as so
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc

def getvalue(params,key,default=None):
	try:
		if params[key]!=default:
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
			value=getvalue(params,'value','')
			locatortype=getvalue(params,'type','')
			acutid=getvalue(params,'acutid','')
			DESC=getvalue(params,'DESC')
			if value.strip()=='' or locatortype.strip()=='' or acutid=='':
				self.write('failed,key params not complete')
				so.userlog.error('key params not complete')
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
			so.userlog.error(str(e))
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
				return
			value=getvalue(params,'value',None)
			locatortype=getvalue(params,'type',None)
			acutid=getvalue(params,'acutid',None)
			DESC=getvalue(params,'DESC',None)
			sess=so.Session()
			locators=sess.query(Locator).filter(Locator.ID==_id).all()
			if len(locators)==0:
				so.userlog.info('locator not exist')
				self.write(failed,'locator not exist')
				return
			locator=locators[0]
			if str(value).strip()=='' or str(locatortype).strip()=='' or str(acutid).strip()=='':
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
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

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
				returnlist.append([int(r.ID),'$$##'+r.Value,'$$##'+r.LocatorType.Name,'$$##'+r.ACUT.Name+':'+r.ACUT.Version+"("+r.ACUT.ACUTType.Name+")",'$$##'+str(r.DESC).decode('utf8')])
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
			ids=[int(x) for x in data.split('=')[1].split(',')]
			res={}
			sess=so.Session()
			for x in ids:
				try:
					sess.query(Locator).filter(Locator.ID==int(x)).delete()
					res[x]='success'
				except:
					so.userlog.error('delete locator:'+str(x)+' failed')
					res[x]='failed'
			sess.commit()
			so.userlog.info('delete locator:'+str(res))
			self.write(str(res).replace('None','null'))
		except Exception,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
		