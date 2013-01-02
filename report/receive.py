#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

import pika,time
from atplatform.report import commonparam as cp
from atplatform.report.planresult import planresult
from atplatform.report import sharedobject as so
import traceback
from atplatform.report.mappedtable import *
import time

def callback(ch, method, properties, body):
	tempplanresult=None
	try:
		tempplanresult=planresult(body)
		insertreport(tempplanresult.planname)
		ch.basic_ack(delivery_tag = method.delivery_tag)
		if tempplanresult.valid==False:
			setreportstatus(tempplanresult.planname,so.reportstatus[3])
			return
		setreportstatus(tempplanresult.planname,so.reportstatus[1])
		tempplanresult.generatereport()
		setreportstatus(tempplanresult.planname,so.reportstatus[2])
		setreportgeneratedtime(tempplanresult.planname)
	except Exception,e:
		planname=None
		if tempplanresult!=None:
			try:
				planname=str(tempplanresult.planname)
				setreportstatus(tempplanresult.planname,so.reportstatus[3])
			except:
				pass
		so.processlog.error('error occured during process report for plan:'+str(planname)+',error:'+traceback.format_exc())

def getlistening():
	try:
		connection = pika.BlockingConnection(pika.ConnectionParameters(
			host=cp.mqhost))
		channel = connection.channel()
		channel.queue_declare(queue='sendresult', durable=True)
		channel.basic_qos(prefetch_count=1)
		channel.basic_consume(callback,
							  queue='sendresult')
		so.adminlog.info('server started and ready to receive raw plan result')
		channel.start_consuming()
	except Exception,e:
		so.processlog.critical('main MQ listening thread occured a error:'+traceback.format_exc()+',traceback:'+traceback.format_exc())

def setreportstatus(planname,reportstatus):
	s=None
	try:
		s=so.Session()
		res=s.query(Report).join(Report.Plan).filter(Plan.Name==str(planname))
		res=res.one()
		res.ReportStatus=s.query(ReportStatus).filter(ReportStatus.Name==str(reportstatus)).one()
		s.commit()
		s.close()
	except Exception,e:
		if s!=None:
			s.rollback()
			s.close()
		so.processlog.error('error occured during setreportstatus,planname:'+str(planname)+' reportstatus:'+str(reportstatus)+',traceback:'+traceback.format_exc())

def insertreport(planname):
	s=None
	try:
		s=so.Session()
		status=s.query(ReportStatus).filter(ReportStatus.Name==str(so.reportstatus[0])).one()
		re=Report(planname)
		re.Plan=s.query(Plan).filter(Plan.Name==str(planname)).one()
		re.ReportStatus=status
		s.add(re)
		s.commit()
		s.close()
	except Exception,e:
		if s!=None:
			s.rollback()
			s.close()
		so.processlog.error('error occured during insert report to db,planname:'+str(planname)+',traceback:'+traceback.format_exc())
		raise Exception(traceback.format_exc())

def setreportgeneratedtime(name):
	s=None
	try:
		s=so.Session()
		res=s.query(Report).filter(Report.Name==str(name))
		res=res.one()
		res.GeneratedTime=int(time.time())
		s.commit()
		s.close()
	except Exception,e:
		if s!=None:
			s.rollback()
			s.close()
		so.processlog.error('error occured during setreportgeneratedtime,planname:'+str(name)+',traceback:'+traceback.format_exc())
