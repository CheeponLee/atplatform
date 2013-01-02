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
			s=so.Session()
			res=s.query(LocatorType).all()
			s.commit()
			returnlist=[];
			for r in res:
				returnlist.append(('$$##'+r.Name).decode('utf8'))
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error(str(e))
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()