#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from  atplatform.report import commonparam as cp
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

processlog=None
userlog=None
adminlog=None


Base=None
metadata=None
Session=None
engine=None
pool=None


def Init():
	global Base,metadata,engine,Session
	Base=declarative_base()
	metadata=MetaData()
	engine=create_engine(cp.Connect_string,pool_size=cp.dbpoolsize,max_overflow=0,pool_timeout=cp.dbpool_timeout,pool_recycle=cp.dbpool_recycle,echo=cp.dbecho)
	Session = sessionmaker(bind=engine)
	metadata.reflect(bind=engine)

reportstatus=['inited','generatingreport','generatereportdone','error']