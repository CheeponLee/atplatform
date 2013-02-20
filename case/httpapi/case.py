#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import tornado.web
import os
import urllib
import re
from atplatform.case import sharedobject as so
from atplatform.case import commonparam as cp
from atplatform.case.mappedtable import *
from sqlalchemy.exc import *
from sqlalchemy import desc
import traceback

def getvalue(params,key,default=None):
	try:
		if params[key]!=default:
			return params[key]
		else:
			return default
	except:
		return default

class search(tornado.web.RequestHandler):
	def get(self,argv):
		try:
			s=None
			_id = self.get_argument("id" , None) 
			if _id==None:
				name = self.get_argument("name",None)
				name_searchstyle=self.confirmsearchstyle(self.get_argument("name_searchstyle",'like'))
				preplansum = self.get_argument("preplansum",-1)
				postplansum = self.get_argument("postplansum",None)
				preacutsum = self.get_argument("preacutsum",-1)
				postacutsum = self.get_argument("postacutsum",None)
				pretimerange = self.get_argument("pretimerange",-1)
				posttimerange = self.get_argument("posttimerange",None)
			else:
				name=None
				preplansum=-1
				postplansum=None
				preacutsum=-1
				postacutsum=None
				pretimerange = -1
				posttimerange =None
			_range = self.get_argument("range",None)
			s=so.Session()
			res=s.query(Case)
			if _id!=None:
				res=res.filter(Case.ID==int(_id))
			returnlist=[]
			if name==None and preplansum == -1 and postplansum==None and preacutsum == -1 and postacutsum==None and pretimerange==-1 and posttimerange==None:
				pass
			else:
				if name!=None and name!='':
					res=eval('res.filter(Case.Name.'+name_searchstyle+'(name))')
				if postplansum!=None:
					res=res.filter(Case.ReferencedPlanSUM>=preplansum,Case.ReferencedPlanSUM<=postplansum)
				else:
					res=res.filter(Case.ReferencedPlanSUM>=preplansum)
				if postacutsum!=None:
					res=res.filter(Case.ReferencedACUTSUM>=preacutsum,Case.ReferencedACUTSUM<=postacutsum)
				else:
					res=res.filter(Case.ReferencedACUTSUM>=preacutsum)
				if posttimerange!=None:
					res=res.filter(Case.LastModifyTime>=pretimerange,Case.ReferencedPlanSUM<=posttimerange)
				else:
					res=res.filter(Case.LastModifyTime>=pretimerange)
			res=res.order_by(desc(Case.LastModifyTime))
			returnlist.append(int(res.count()))
			if _range!=None:
				_range=[int(x) for x in _range.split(',')]
				res=res[_range[0]:_range[1]]
			else:
				res=res.all()
			s.commit()
			for r in res:
				returnlist.append([int(r.ID),'$$##'+r.Name,'$$##'+r.CaseStatus.Name,int(r.ReferencedPlanSUM),int(r.ReferencedACUTSUM),int(r.LastModifyTime)])
			so.userlog.info('return '+str(len(res))+' cases')
			self.write(str(returnlist).replace('None','null').replace("u'$$##","'"))
		except Exception,e:
			so.userlog.error('error occured during search case,traceback:'+str(traceback.format_exc()))
			if s!=None:
				s.rollback()
			self.write('failed')
		finally:
			if s!=None:
				s.close()

	def confirmsearchstyle(self,style):
		if style!='like':
			return "op('regexp')"
		else:
			return 'like'

class ban(tornado.web.RequestHandler):
	def post(self,argv):
		sess=None
		try:
			data=urllib.unquote(self.request.body)
			params=dict([x.split('=') for x in data.split('&')])
			ids=getvalue(params,'ids')
			banstr=getvalue(params,'banstr')
			if banstr==None or banstr.strip()=='' or ids==None or ids.strip()=='':
				self.write('failed,some params missing')
				return
			if banstr not in ['enable','disable']:
				self.write('failed,banstr error')
				return
			ids=[int(x) for x in ids.split(',')]
			sess=so.Session()
			casestatus_id=sess.query(CaseStatus.ID).filter(CaseStatus.Name==banstr+'d').one().ID
			inusing_casestatus_id=sess.query(CaseStatus.ID).filter(CaseStatus.Name=='inusing').one().ID
			res=sess.query(Case).filter(Case.ID.in_(ids),Case.CaseStatus_ID!=inusing_casestatus_id).update({Case.CaseStatus_ID:casestatus_id},synchronize_session=False)
			sess.commit()
			if res!=0:
				self.write('success')
				so.userlog.info('success set casestatus for case:'+str(ids)+',CaseStatus:'+str(banstr)+'d')
			else:
				self.write('failed,check if the case exist')
				so.userlog.error('failed set casestatus for case:'+str(ids)+',CaseStatus:'+str(banstr)+'d, the cases may does not exist')
		except Exception,e:
			so.userlog.error('error occured during set case status,traceback:'+str(traceback.format_exc()))
			if sess!=None:
				sess.rollback()
			self.write('failed')
		finally:
			if sess!=None:
				sess.close()
		