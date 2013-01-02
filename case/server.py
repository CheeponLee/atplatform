#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import os
import sys
reload(sys)
curdir=os.getcwd()
if not curdir[:-4] in sys.path :
	sys.path.append(curdir[:-4])

from atplatform.case import commonparam as cp
import tornado.ioloop
import tornado.web
import atplatform.case.sharedobject as so
from atplatform.case import testlogging

if __name__ == "__main__":
	so.Init()
try:
	from atplatform.case.mappedtable import *
except:
	pass
from atplatform.case.testlogging import *
sys.setdefaultencoding('utf8')
from atplatform.case.uploadcase import uploadcase

urls = [
	('/uploadcase(.*)', uploadcase)
]

if __name__ == "__main__":
	testlogging.init()
	application = tornado.web.Application(urls, globals())
	application.listen(cp.uploadcaseport)
	tornado.ioloop.IOLoop.instance().start()