#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import atplatform.wc.sharedobject as so
from sqlalchemy.orm import relationship, backref

class  AUT(so.Base):
	"""docstring for  AUT"""
	__table__ = so.metadata.tables['aut']

	AUTType = relationship('AUTType',backref="AUT")
	ACUT = relationship('ACUT', secondary=so.metadata.tables['aut_has_acut'], backref='AUT')

	def __init__(self,Name,DESC=None):
		super( AUT, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  AUTType(so.Base):
	"""docstring for  AutType"""
	__table__ = so.metadata.tables['auttype']
	def __init__(self,Name,DESC=None):
		super( AUTType, self).__init__()
		self.Name=Name
		self.DESC=DESC

class  ACUT(so.Base):
	__table__ = so.metadata.tables['acut']
	ACUTType = relationship('ACUTType',backref="ACUT")
	Locator=relationship('Locator',backref="ACUT")
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