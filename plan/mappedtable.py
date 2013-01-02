#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import atplatform.plan.sharedobject as so
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

class  Case(so.Base):
	__table__ = so.metadata.tables['case']
	CaseStatus = relationship('CaseStatus',backref="Case")
	
	def __init__(self,Name,DESC=None):
		super( Case, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  CaseStatus(so.Base):
	__table__ = so.metadata.tables['casestatus']
	def __init__(self,Name,DESC=None):
		super( PlanStatus, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  Platform(so.Base):
	__table__ = so.metadata.tables['platform']

	def __init__(self,Name):
		super( Platform, self).__init__()
		self.Name=Name

class  Browser(so.Base):
	"""docstring for  Browser"""
	__table__ = so.metadata.tables['browser']

	Platform = relationship('Platform', secondary=so.metadata.tables['browser_on_platform'], backref='Browser')

	def __init__(self,Name,Version=''):
		super( Browser, self).__init__()
		self.Name=Name
		self.Version=Version

class  Case_in_Plan(so.Base):
	"""docstring for  Case_in_Plan"""
	__table__ = so.metadata.tables['case_in_plan']

	Case = relationship('Case',backref="Case_in_Plan")

	Plan = relationship('Plan',backref=backref("Case_in_Plan",cascade='all, delete-orphan'))

	#secondarytable=so.metadata.tables['browser_on_platform']

	#Browser_on_Platform = relationship('Browser_on_Platform', secondary=so.metadata.tables['case_in_plan_browser_on_platform_rel'],primaryjoin=and_('pages.c.id==pages.c.parent_id'),remote_side='Page.id',, backref='Case_in_Plan')
	Browser_on_Platform = relationship('Browser_on_Platform', secondary=so.metadata.tables['case_in_plan_browser_on_platform_rel'], backref='Case_in_Plan')

	def __init__(self):
		super( Case_in_Plan, self).__init__()

class  Browser_on_Platform(so.Base):
	"""docstring for  Browser_on_Platform"""
	__table__ = so.metadata.tables['browser_on_platform']

	Browser = relationship('Browser',backref="Browser_on_Platform")

	Platform = relationship('Platform',backref="Browser_on_Platform")

	Browser_on_Platform_Status=relationship('Browser_on_Platform_Status',backref="Browser_on_Platform")

	def __init__(self):
		super( Browser_on_Platform, self).__init__()

class  Browser_on_Platform_Status(so.Base):
	"""docstring for  Browser_on_Platform_Status"""
	__table__ = so.metadata.tables['browser_on_platform_status']
	
	def __init__(self):
		super( Browser_on_Platform_Status, self).__init__()

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
