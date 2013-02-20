#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import urllib
from atplatform.wc import sharedobject as so
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
import re
import traceback

def getvalue(params,key,default=None):
	try:
		if params[key]!='':
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
			name=_strip(getvalue(params,'name'))
			version=_strip(getvalue(params,'version','1.0'))
			auttype=getvalue(params,'auttype','website')
			acut=getvalue(params,'acut')
			DESC=getvalue(params,'DESC')
			vali_res=self.validation(name,version,DESC)
			if vali_res!='pass':
				return
			sess=so.Session()
			newaut=AUT(name)
			newaut.Version=version
			newaut.DESC=DESC
			newaut.AUTType=sess.query(AUTType).filter(AUTType.Name==auttype).one()
			if (acut!=None):
				acutlist=[]
				for x in acut.split(','):
					acutlist.append(sess.query(ACUT).filter(ACUT.ID==x).one())
				newaut.ACUT=acutlist
			sess.add(newaut)
			sess.commit()
			self.write('success,'+str(newaut.ID))
			so.userlog.info('add aut success,autid='+str(newaut.ID))
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during add aut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

	def validation(self,name,version,DESC):
		if name==None:
			self.write('failed,name is null')
			so.userlog.error('autname is None')
			return 'not pass'
		if version==None:
			self.write('failed,aut version is null')
			so.userlog.error('aut version is None')
			return 'not pass'
		regexpstr="^[\\x41-\\x5a,\\x61-\\x7a,\\x5f][\\s,\\x41-\\x5a,\\x61-\\x7a,\\x30-\\x39,\\x5f]*$"
		if re.match(regexpstr,name)==None:
			self.write('failed,name illegal')
			so.userlog.error('autname illegal')
			return 'not pass'
		if len(name)>45:
			self.write('failed,autname too long')
			so.userlog.error('autname too long')
			return 'not pass'
		if len(version)>45:
			self.write('failed,,version too long')
			so.userlog.error('version too long')
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
			name=_strip(getvalue(params,'name'))
			version=_strip(getvalue(params,'version'))
			DESC=getvalue(params,'DESC')
			addacut=getvalue(params,'addacut')
			deleteacut=getvalue(params,'deleteacut')
			vali_res=self.validation(_id,name,version,DESC)
			if vali_res!='pass':
				return
			sess=so.Session()
			auts=sess.query(AUT).filter(AUT.ID==_id).all()
			if len(auts)==0:
				self.write(failed,'aut not exist')
				so.userlog.info('aut not exist')
				return
			aut=auts[0]
			if name=='' or version=='':
				self.write('failed,cannot set key property empty')
				so.userlog.error('cannot set key property empty')
				return
			if name!=None:
				aut.Name=name
			if version!=None:
				aut.Version=version
			if DESC!=None:
				aut.DESC=DESC
			if addacut!=None:
				for x in addacut.split(','):
					aut.ACUT.append(sess.query(ACUT).filter(ACUT.ID==int(x)).one())
			if deleteacut!=None:
				for x in deleteacut.split(','):
					aut.ACUT.remove(sess.query(ACUT).filter(ACUT.ID==int(x)).one())
			sess.commit()
			self.write('success')
			so.userlog.info('modify aut success')
		except IntegrityError,e:
			so.userlog.error(str(e))
			if sess!=None:
				sess.rollback()
			self.write('failed,params conflict')
		except Exception,e:
			so.userlog.error('error occured during modify aut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

	def validation(self,_id,name,version,DESC):
		if _id==None:
			self.write("failed,id is not given")
			so.userlog.error('id is not given')
			return 'not pass'
		if name==None:
			self.write('failed,name is null')
			so.userlog.error('autname is None')
			return 'not pass'
		if version==None:
			self.write('failed,aut version is null')
			so.userlog.error('aut version is None')
			return 'not pass'
		regexpstr="^[\\x41-\\x5a,\\x61-\\x7a,\\x5f][\\s,\\x41-\\x5a,\\x61-\\x7a,\\x30-\\x39,\\x5f]*$"
		if re.match(regexpstr,name)==None:
			self.write('failed,name illegal')
			so.userlog.error('autname illegal')
			return 'not pass'
		if len(name)>45:
			self.write('failed,autname too long')
			so.userlog.error('autname too long')
			return 'not pass'
		if len(version)>45:
			self.write('failed,,version too long')
			so.userlog.error('version too long')
			return 'not pass'
		if DESC!=None and len(DESC)>200:
			self.write('failed,DESC too long')
			so.userlog.error('DESC too long')
			return 'not pass'
		return 'pass'

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
				#auttype = self.get_argument("auttype",None)
				preacutsum = self.get_argument("preacutsum",-1)
				postacutsum = self.get_argument("postacutsum",None)
				DESC = self.get_argument("DESC",None)
				desc_searchstyle=self.confirmsearchstyle(self.get_argument("desc_searchstyle",'like'))
			else:
				name=None
				version = None
				preacutsum = -1
				postacutsum=None
				DESC=None
			_range = self.get_argument("range",None)
			s=so.Session()
			res=s.query(AUT)
			if _id!=None:
				res=res.filter(AUT.ID==int(_id))
			returnlist=[]
			if name==None and version == None and preacutsum == -1 and postacutsum==None and DESC==None:
				pass
			else:
				if name!=None and name!='':
					res=eval('res.filter(AUT.Name.'+name_searchstyle+'(name))')
				if version!=None and version!='':
					res=eval('res.filter(AUT.Version.'+version_searchstyle+'(version))')
				if postacutsum!=None:
					res=res.filter(AUT.ACUTSUM>=preacutsum,AUT.ACUTSUM<=postacutsum)
				else:
					res=res.filter(AUT.ACUTSUM>=preacutsum)
				if DESC!=None and DESC!='':
					res=eval('res.filter(AUT.DESC.'+desc_searchstyle+'(DESC))')
			res=res.order_by(desc(AUT.LastModifyTime))
			returnlist.append(int(res.count()))
			if _range!=None:
				_range=[int(x) for x in _range.split(',')]
				res=res[_range[0]:_range[1]]
			else:
				res=res.all()
			s.commit()
			for r in res:
				returnlist.append([int(r.ID),'$$##'+r.Name,'$$##'+r.Version,int(r.ACUTSUM),'$$##'+str(r.DESC).decode('utf8')])
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
			so.userlog.info('return '+str(len(res))+' auts')
		except Exception,e:
			so.userlog.error('error occured during search aut,traceback:'+str(traceback.format_exc()))
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
					sess.query(AUT).filter(AUT.ID==int(x)).delete()
					res[x]='success'
				except:
					so.userlog.error('delete aut:'+str(x)+' failed')
					res[x]='failed'
			sess.commit()
			self.write(str(res).replace('None','null'))
			so.userlog.info('delete aut:'+str(res))
		except Exception,e:
			so.userlog.error('error occured during delete aut,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
		