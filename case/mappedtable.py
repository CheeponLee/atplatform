#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import atplatform.case.sharedobject as so
from sqlalchemy.orm import relationship, backref

class  ACUT(so.Base):
	__table__ = so.metadata.tables['acut']
	ACUTType = relationship('ACUTType',backref="ACUT")

	def __init__(self,Name,DESC=None):
		super( ACUT, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  ACUTType(so.Base):
	__table__ = so.metadata.tables['acuttype']
	def __init__(self,Name,DESC=None):
		super( ACUTType, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  Case(so.Base):
	__table__ = so.metadata.tables['case']
	CaseStatus=relationship('CaseStatus',backref="Case")

	def __init__(self,Name,DESC=None):
		super( Case, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  CaseStatus(so.Base):
	__table__ = so.metadata.tables['casestatus']

	def __init__(self,Name,DESC=None):
		super( CaseStatus, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  Locator(so.Base):
	__table__ = so.metadata.tables['locator']
	LocatorType = relationship('LocatorType',backref="Locator")

	def __init__(self,Value):
		super( Locator, self).__init__()
		self.Value=Value

class  LocatorType(so.Base):
	__table__ = so.metadata.tables['locatortype']

	def __init__(self,Name,DESC=None):
		super( LocatorType, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  ACUT_Locator_Case_rel(so.Base):
	__table__ = so.metadata.tables['acut_locator_case_rel']
	ACUT = relationship('ACUT',backref=backref("ACUT_Locator_Case_rel",cascade='all, delete-orphan'))
	Locator = relationship('Locator',backref=backref("ACUT_Locator_Case_rel",cascade='all, delete-orphan'))
	Case = relationship('Case',backref=backref("ACUT_Locator_Case_rel",cascade='all, delete-orphan'))

	def __init__(self):
		super( ACUT_Locator_Case_rel, self).__init__()