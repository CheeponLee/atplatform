#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import functools
import traceback
from multiprocessing import Process,Queue,Value, Array
import atplatform.plan.sharedobject as so

def exceptioncatch(func):
	@functools.wraps(func)
	def wrappedFunc(*arg,**argd):
		try:
			func(*arg,**argd)
		except Exception, e:
			message=traceback.format_exc()
			if len(e.args)!=2:
				arg[-1].put(['failed',message,''])
			else:
				arg[-1].put(['failed',message,e.args[1]])
			return
		arg[-1].put(['success','',''])
	return wrappedFunc