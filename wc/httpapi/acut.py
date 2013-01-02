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
			so.userlog.error(str(e))
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
					sess.query(ACUT).filter(ACUT.ID==int(x)).delete()
					res[x]='success'
				except:
					so.userlog.error('delete acut:'+str(x)+' failed')
					res[x]='failed'
			sess.commit()
			so.userlog.info('delete acut:'+str(res))
			self.write(str(res).replace('None','null'))
		except Exception,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
		