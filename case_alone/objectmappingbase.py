#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
try:
	import atplatform.plan.commonparam as cp
except:
	import commonparam as cp
import httplib
from lxml import etree
from selenium.common.exceptions import StaleElementReferenceException
import functools
import traceback

class CheckedWebElement(object):
	def __init__(self, driver,acuttype,locator):
		self.driver=driver
		self.locator=locator
		self.type=acuttype
		self.obj=None
		self.invokeflag=False

	def __getattribute__(self,name):
		if name!='driver' and name!='locator' and name!='obj' and name!='invokeflag' and name!='type' and name!='__init__' and name!='wrapfunc' and name!='getobjconnection':
			if self.invokeflag==True:
				return eval('self.obj.'+name)
			else:
				self.getobjconnection()
				return eval('self.obj.'+name)
		else:
			return object.__getattribute__(self,name)

	def wrapfunc(self,func):
		@functools.wraps(func)
		def wrappedFunc(*arg,**argd):
			try:
				return func(*arg,**argd)
			except StaleElementReferenceException:
				func.im_self.upperhandle.invokeflag=False
				func.im_self.upperhandle.getobjconnection()
				func.im_self.upperhandle.__getattribute__(func.__name__)(*arg,**argd)
		return wrappedFunc

	def getobjconnection(self):
		self.obj=eval('self.driver.'+so.locatormapping[self.locator[0]].replace('S',(self.type==so.acuttype[1])*'s')+'(\''+self.locator[1]+'\')')
		members=dir(self.obj)
		methodmembers=[]
		for i in members:
			if repr(eval('self.obj.'+i)).find('method')!=-1 and repr(eval('self.obj.'+i)).find('__')==-1:
				methodmembers.append(i)
		for i in methodmembers:
			exec('self.obj.'+i+'=self.wrapfunc(self.obj.'+i+')')
		#put this class object handle to the raw class object
		self.obj.upperhandle=self
		self.invokeflag=True


def search(driver,acutid,locatorid):
	locatorres=remotegetlocator(locatorid)
	acuttyperes=remotegetacuttype(acutid)
	if locatorres==False or acuttyperes==False:
		raise Exception('Get locator or acuttype Error')
	else:
		obj=CheckedWebElement(driver,acuttyperes,locatorres)
		return obj


def remotegetlocator(locatorid):
	try:
		conn = httplib.HTTPConnection(cp.acutlibhost)
		headers = {"Content-Type":"text/xml; charset=utf8"}
		conn.request('GET', '/locator.search?id='+str(locatorid),headers=headers)
		res=conn.getresponse()
		res=res.read()
		conn.close()
		res=eval(res)
		if res[0]==0:
			raise Exception('Get locator failed')
		else:
			return (res[1][2],res[1][1])
	except Exception,e:
		print 'get remote locator failed,id:'+str(locatorid)+',traceback:'+traceback.format_exc()
		return False

def remotegetacuttype(acutid):
	try:
		conn = httplib.HTTPConnection(cp.acutlibhost)
		headers = {"Content-Type":"text/xml; charset=utf8"}
		conn.request('GET', '/acut.search?id='+str(acutid),headers=headers)
		res=conn.getresponse()
		res=res.read()
		conn.close()
		res=eval(res)
		if res[0]==0:
			raise Exception('Get acuttype failed')
		else:
			return res[1][3]
	except:
		print 'get remote acuttype failed,id:'+str(acutid)+',traceback:'+traceback.format_exc()
		return False