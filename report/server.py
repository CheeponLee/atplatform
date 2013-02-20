#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.ioloop
import tornado.web
import traceback
import logging
from lxml import etree
import os
import gc
import time
import thread
import sys
reload(sys)
sys.path.append('/home/uls/workplace/atplatform/')
import thread
from atplatform.report import sharedobject as so
if __name__ == "__main__":
	so.Init()
from atplatform.report import receive
from  atplatform.report import testlogging
sys.setdefaultencoding('utf8')
try:
	from atplatform.plan.mappedtable import *
except:
	pass
from  atplatform.report import commonparam as cp

class StaticWWWHandler(tornado.web.StaticFileHandler):
	def initialize(self, path, default_filename=None):
		self.root = os.path.abspath(path) + os.path.sep
		self.default_filename = default_filename

urls = [
	('/www/(.*)',StaticWWWHandler,dict(path=cp.reporthome+'static/results/'))]


if __name__ == "__main__":
	testlogging.init(logging.DEBUG)
	thread.start_new_thread(receive.getlistening,())
	application = tornado.web.Application(urls, globals())
	application.listen(776)
	tornado.ioloop.IOLoop.instance().start()

#plan1::planinfo::[('case2', {'Webdriverhub': 'http://localhost:4444/wd/hub', 'Browserversion': '', 'Javascriptenabled': 'True', 'ignoreProtectedModeSettings': True, 'Platform': 'WINDOWS', 'Browsername': 'chrome', 'Findtimeout': 10}), ('case2', {'Webdriverhub': 'http://localhost:4444/wd/hub', 'Browserversion': '', 'Javascriptenabled': 'True', 'ignoreProtectedModeSettings': True, 'Platform': 'WINDOWS', 'Browsername': 'chrome', 'Findtimeout': 10})]|||2,[1347980467.001, 1347980472.001, 1347980489.044]|||workerinfo:{'case2__2012-09-18__Tuesday__23.01.12__\xe4\xb8\xad\xe5\x9b\xbd\xe6\xa0\x87\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4': ['stopped', 1347980472.893, 1347980479.337, 'failed', 'Traceback (most recent call last):\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\runengine\\exceptioncatch.py", line 11, in wrappedFunc\n    func(*arg,**argd)\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\runengine\\execute.py", line 22, in exec_case\n    case.init()\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\cases\\case2\\case2.py", line 19, in init\n    om.gWebelement()\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\cases\\case2\\objectmapping.py", line 16, in gWebelement\n    q=ombase.search(driver,5,1)\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\objectmappingbase.py", line 57, in search\n    raise Exception(\'Get locator or acuttype Error\')\nException: Get locator or acuttype Error\n', ''], 'case2__2012-09-18__Tuesday__23.01.14__\xe4\xb8\xad\xe5\x9b\xbd\xe6\xa0\x87\xe5\x87\x86\xe6\x97\xb6\xe9\x97\xb4': ['stopped', 1347980482.913, 1347980489.044, 'failed', 'Traceback (most recent call last):\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\runengine\\exceptioncatch.py", line 11, in wrappedFunc\n    func(*arg,**argd)\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\runengine\\execute.py", line 22, in exec_case\n    case.init()\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\cases\\case2\\case2.py", line 19, in init\n    om.gWebelement()\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\cases\\case2\\objectmapping.py", line 16, in gWebelement\n    q=ombase.search(driver,5,1)\n  File "C:\\Users\\Cheepon\\Desktop\\lab\\temp\\objectmappingbase.py", line 57, in search\n    raise Exception(\'Get locator or acuttype Error\')\nException: Get locator or acuttype Error\n', '']}