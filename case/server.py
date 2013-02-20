#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import os
import sys
reload(sys)
sys.path.append('/home/uls/workplace/atplatform/')

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
from atplatform.case.httpapi import *

class StaticWWWHandler(tornado.web.StaticFileHandler):
	def initialize(self, path, default_filename=None):
		self.root = os.path.abspath(path) + os.path.sep
		self.default_filename = default_filename

urls = [
	('/www/(.*)',StaticWWWHandler,dict(path=cp.home+'static/')),
	('/uploadcase(.*)', uploadcase.uploadcase),
	('/updatecasefiles(.*)', updatecasefiles.updatecasefiles),
	('/case.search(.*)', case.search),
	('/case.ban(.*)', case.ban)
]

if __name__ == "__main__":
	testlogging.init()
	application = tornado.web.Application(urls, globals())
	application.listen(cp.uploadcaseport)
	tornado.ioloop.IOLoop.instance().start()