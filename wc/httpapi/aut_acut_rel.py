#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
from atplatform.wc import sharedobject as so
from atplatform.wc.mappedtable import *
from sqlalchemy.exc import *

#http://localhost:774/locator.search?value=95&type=&value_searchstyle=regexp&range=1,20
class search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=None
			autid = self.get_argument("autid",None)
			acutid = self.get_argument("acutid",None)
			_range = self.get_argument("range",None)
			returnlist=[]
			if autid==None and  acutid==None:
				so.userlog.info('failed,aut and acut cannot be None at the same time')
				self.write("failed,aut and acut cannot be None at the same time")
				return
			if autid!=None and  acutid!=None:
				so.userlog.info('failed,aut and acut cannot be notNone at the same time')
				self.write("failed,aut and acut cannot be notNone at the same time")
				return
			s=so.Session()
			if autid!=None:
				res=s.query(ACUT)
				autidlist=[int(i) for i in autid.split(',')]
				res=res.join(ACUT.AUT).filter(AUT.ID.in_(autidlist))
			else:
				res=s.query(AUT)
				acutidlist=[int(i) for i in acutid.split(',')]
				res=res.join(AUT.ACUT).filter(ACUT.ID.in_(acutidlist))
			returnlist.append(int(res.count()))
			if _range!=None:
				_range=[int(x) for x in _range.split(',')]
				res=res[_range[0]:_range[1]]
			else:
				res=res.all()
			s.commit()
			for r in res:
				returnlist.append(int(r.ID))
			so.userlog.info('return '+str(len(res))+' rel')
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()