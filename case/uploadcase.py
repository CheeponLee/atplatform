#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

import tornado.web
import urllib
from atplatform.case import sharedobject as so
from atplatform.case.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
import shutil
import re
import zipfile
import time
import random
import os
import traceback

class uploadcase(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		tmpdirname=str(int(time.time()*1000))+str(random.randint(1,1000))
		try:
			data=urllib.unquote(self.request.body)
			data
			filepath=re.search('(?<=path.\n).*(?=\n)',data).group()
			filename=re.search('(?<=name.\n).*(?=\n)',data).group()
			print filepath,filename
			if zipfile.is_zipfile(filepath):
				zipf=zipfile.ZipFile(filepath)
				os.mkdir(cp.tmpdir+tmpdirname)
				zipf.extractall(cp.tmpdir+tmpdirname)
				dirlist=os.listdir(cp.tmpdir+tmpdirname)
				if len(dirlist)>cp.maxuploadcase:
					self.write('too many cases')
					so.userlog.error('too many cases,'+str(len(dirlist))+'>'+str(cp.maxuploadcase))
					shutil.rmtree(cp.tmpdir+tmpdirname)
					return
				else:
					self.write('checksucess')
					return
			else:
				self.write('upload file is not a zip file')
				so.userlog.error('upload file is not a zip file,filename:'+str(filename))
				return
		except Exception,e:
			so.userlog.error('error occured in uploading case ,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()