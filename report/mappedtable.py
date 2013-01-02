#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import atplatform.report.sharedobject as so
from sqlalchemy.orm import relationship, backref

class  Plan(so.Base):
	"""docstring for  Plan"""
	__table__ = so.metadata.tables['plan']

	PlanStatus = relationship('PlanStatus',backref="Plan")

	def __init__(self,Name,DESC=None):
		super( Plan, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  PlanStatus(so.Base):
	"""docstring for  PlanStatus"""
	__table__ = so.metadata.tables['plan_status']
	def __init__(self,Name,DESC=None):
		super( PlanStatus, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  Report(so.Base):
	__table__ = so.metadata.tables['report']
	Plan = relationship('Plan',uselist=False,backref="Report")
	ReportStatus=relationship('ReportStatus',backref="Report")

	def __init__(self,Name,DESC=None):
		super( Report, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  ReportStatus(so.Base):
	__table__ = so.metadata.tables['reportstatus']
	def __init__(self,Name,DESC=None):
		super( ReportStatus, self).__init__()
		self.Name=Name
		self.DESC=DESC
