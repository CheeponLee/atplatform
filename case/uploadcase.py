#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

import tornado.web
import urllib
from atplatform.case import sharedobject as so
from atplatform.case.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
from atplatform.case import commonparam as cp
from atplatform.case.mappedtable import *
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
		passedcases=[]
		try:
			data=urllib.unquote(self.request.body)
			filepath=re.search('(?<=path.\r\n\r\n).*(?=\r\n)',data).group()
			filename=re.search('(?<=name.\r\n\r\n).*(?=\r\n)',data).group()
			print filepath,filename
			if zipfile.is_zipfile(filepath):
				zipf=zipfile.ZipFile(filepath)
				os.mkdir(cp.tmpdir+tmpdirname)
				zipf.extractall(cp.tmpdir+tmpdirname)
				dirlist=os.listdir(cp.tmpdir+tmpdirname)
				if len(dirlist)>cp.maxuploadcase:
					self.write('too many cases')
					so.userlog.error('too many cases,'+str(len(dirlist))+'>'+str(cp.maxuploadcase))
				else:
					sess=so.Session()
					for ca in dirlist:
						res=self.addcase(tmpdirname,ca,sess)
						if res==True:
							passedcases.append(ca)
				shutil.rmtree(cp.tmpdir+tmpdirname)
				if len(passedcases)==len(dirlist):
					self.write('all cases uploaded success')
				else:
					self.write('upload success cases:'+','.join(passedcases))
			else:
				self.write('upload file is not a zip file')
				so.userlog.error('upload file is not a zip file,filename:'+str(filename))
		except Exception,e:
			so.userlog.error('error occured in uploading case ,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			if os.path.exists(cp.tmpdir+tmpdirname):
				shutil.rmtree(cp.tmpdir+tmpdirname)
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()

	def get_relation(self,acut_locator_list,mappingpath,s):
		f=None
		try:
			f=file(mappingpath,'r')
			rf=f.readline()
			while(rf!=''):
				res=re.search(r'(?<=search\(driver,)\d+,\d+(?=\))',rf)
				if res!=None:
					pair=res.group().split(',')
					acut_locator_list.append(pair)
				rf=f.readline()
			f.close()
		except:
			if f!=None:
				f.close()

	def addcase(self,tmpdirname,ca,sess):
		try:
			res=re.match(r'^[\x41-\x5a,\x61-\x7a][\x41-\x5a,\x61-\x7a,\x30-\x39,\x5f]*$',ca)
			if res!=None and os.path.isdir(cp.tmpdir+tmpdirname+'/'+ca) and os.path.exists(cp.tmpdir+tmpdirname+'/'+ca+'/'+ca+'.py'):
				acut_locator_list=[]
				sess=so.Session()
				if os.path.exists(cp.tmpdir+tmpdirname+'/'+ca+'/'+'objectmapping.py'):
					self.get_relation(acut_locator_list,cp.tmpdir+tmpdirname+'/'+ca+'/'+'objectmapping.py',sess)
				casestatus=sess.query(CaseStatus).filter(CaseStatus.Name==so.casestatus[1]).one()
				c=Case(ca)
				c.CaseStatus=casestatus
				sess.add(c)
				for r in acut_locator_list:
					rel=ACUT_Locator_Case_rel()
					rel.ACUT_ID=r[0]
					rel.Locator_ID=r[1]
					rel.Case=c
					sess.add(rel)
				shutil.copytree(cp.tmpdir+tmpdirname+'/'+ca+'/',cp.casesdir)
				sess.commit()
				return True
			else:
				return False
		except Exception,e:
			so.userlog.error('error occured in adding case ,traceback:'+str(traceback.format_exc()))
			if os.path.exists(cp.casesdir+ca):
				shutil.rmtree(cp.casesdir+ca)
			if sess!=None:
				sess.rollback()
			return False