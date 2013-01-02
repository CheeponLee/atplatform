#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time 
# import objectmapping as om

class testcasebase(object):
	def __init__(self,config,queue):
		super(testcasebase, self).__init__()
		self.driver=None
		self.browsername=config['Browsername']
		self.browserversion=config['Browserversion']
		self.platform=config['Platform']
		self.findtimeout=config['Findtimeout']
		self.webdriverhub=config['Webdriverhub']
		self.javascriptenabled=config['Javascriptenabled']
		self.ignoreProtectedModeSettings=config['ignoreProtectedModeSettings']
		self.queue=queue

	def init(self):
		#driver=eval('webdriver.'+self.browsername+'()')
		desiredcapabilities={'browserName':self.browsername,'version':self.browserversion,'javascriptEnabled':self.javascriptenabled,'platform':self.platform,'ignoreProtectedModeSettings':self.ignoreProtectedModeSettings}
		driver=webdriver.Remote(self.webdriverhub, desiredcapabilities)
		self.driver=driver
		self.driver.implicitly_wait(self.findtimeout)
		self.queue.put(self.driver)

	def before(self):
		pass

	def action(self):
		pass

	def clean(self):
		pass