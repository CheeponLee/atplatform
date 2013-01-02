#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import atplatform.case.sharedobject as so
from sqlalchemy.orm import relationship, backref

class  ACUT(so.Base):
	__table__ = so.metadata.tables['acut']
	ACUTType = relationship('ACUTType',backref="ACUT")
	Case = relationship('Case', secondary=so.metadata.tables['case_acut_rel'], backref='ACUT')

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