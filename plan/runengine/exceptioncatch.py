#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import functools
import traceback
from multiprocessing import Process,Queue,Value, Array

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
				picmsg=''
				try:
					picmsg=str(e.args[1])
				except:
					pass
				arg[-1].put(['failed',message,picmsg])
			return
		arg[-1].put(['success','',''])
	return wrappedFunc