#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import functools
import traceback
from multiprocessing import Process,Queue,Value, Array
from multiprocessing.queues import Queue as Qclass

def exceptioncatch(func):
	@functools.wraps(func)
	def wrappedFunc(*arg,**argd):
		try:
			func(*arg,**argd)
		except Exception, e:
			message=traceback.format_exc()
			if len(e.args)!=2:
				if isinstance(arg[3],Qclass):
					arg[3].put(['failed',message,''])
				else:
					print "fetal error,error message:::"+message
			else:
				picmsg=''
				try:
					picmsg=str(e.args[1])
				except:
					pass
				if isinstance(arg[3],Qclass):
					arg[3].put(['failed',message,picmsg])
				else:
					print "fetal error,error message:::"+message
			return
		if isinstance(arg[3],Qclass):
			arg[3].put(['success','',''])
		else:
			print "fetal error:arg[3] is not instance of Queue"
	return wrappedFunc