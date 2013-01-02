#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.ioloop
import tornado.web
import sys
reload(sys)
import atplatform.wc.sharedobject as so
from atplatform.wc import testlogging

if __name__ == "__main__":
	so.Init()
try:
	from atplatform.wc.mappedtable import *
except:
	pass
from atplatform.wc.httpapi import *
from atplatform.wc.testlogging import *

sys.setdefaultencoding('utf8')


class checkplanexist(tornado.web.RequestHandler):
	def get(self,argv):
		planname = self.get_argument("planname",None)
		s=so.Session()
		if planname!=None and str(planname).strip()!="":
			rs=s.query(Plan).filter(Plan.Name==planname)
			if rs.count()!=0:
				info=u"plan exist"
			else:
				info=u"plan not exist"
		else:
			info=u"planname is null"
		s.close()
		self.write(str(info).replace('None','null').replace("u'","'"))

urls = [
	('/aut.add(.*)', aut.add),
	('/aut.modify(.*)', aut.modify),
	('/aut.search(.*)', aut.search),
	('/aut.delete(.*)', aut.delete),
	('/locator.add(.*)', locator.add),
	('/locator.modify(.*)', locator.modify),
	('/locator.search(.*)', locator.search),
	('/locator.delete(.*)', locator.delete),
	('/acut.add(.*)', acut.add),
	('/acut.modify(.*)', acut.modify),
	('/acut.search(.*)', acut.search),
	('/acut.delete(.*)', acut.delete),
	('/acuttype.search(.*)', acuttype.search),
	('/locatortype.search(.*)', locatortype.search),
	('/aut_acut_rel.search(.*)', aut_acut_rel.search),
	('/export.aut_search(.*)', export.aut_search),
	('/export.acut_search(.*)', export.acut_search),
	('/export.other_acut_search(.*)', export.other_acut_search),
	('/export.helper(.*)',export.helper),
	('/export.page_helper(.*)',export.page_helper)
]

# def joinplan(p):
# 	time.sleep(30)

if __name__ == "__main__":
	testlogging.init()
	application = tornado.web.Application(urls, globals())
	application.listen(774)
	tornado.ioloop.IOLoop.instance().start()