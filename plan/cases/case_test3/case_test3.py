#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
try:
	import atplatform.plan.objectmapping as om
except:
	import objectmapping as om
try:
	from atplatform.plan.testcasebase import testcasebase
except:
	from testcasebase import testcasebase

class testcase(testcasebase):

	def __init__(self,config,queue):
		testcasebase.__init__(self,config,queue)

	def init(self):
		#driver=eval('webdriver.'+self.browsername+'()')
		testcasebase.init(self)
		om.driver=self.driver
		om.gWebelement()

	def before(self):
		super(testcase,self).before()
		pass

	def action(self):
		om.driver.get('http://yavaeye.com/')
		time.sleep(20)
		print "success"

	def clean(self):
		super(testcase,self).clean()
		om.driver.quit()


if __name__=='__main__':
	config={'Webdriverhub': 'http://localhost:4444/wd/hub', 'Browserversion': '9', 'Javascriptenabled': 'True', 'ignoreProtectedModeSettings': True, 'Platform': 'WINDOWS', 'Browsername': 'IE', 'Findtimeout': 15}
	a=testcase(config,[])
	a.driver=webdriver.Chrome()
	om.driver=a.driver
	om.gWebelement()

	a.before()
	a.action()
	a.clean()