#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from sqlalchemy import *
import atplatform.plan.commonparam as cp
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

userlog=None
adminlog=None
planprogresslog=None
runmanagerlog=None
caseexecuteerrorlog=None

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


acuttype=('web_element','web_elements')
workerstatus=('init','running','stopped','dead','queuing','other')
planstatus=('config all set','wait to run','running','stopped','created')
locatormapping={'xpath':'find_elementS_by_xpath','name':'find_elementS_by_name','id':'find_elementS_by_id','partial_link_text':'find_elementS_by_partial_link_text','link_text':'find_elementS_by_link_text','class_name':'find_elementS_by_class_name','css_selector':'find_elementS_by_css_selector','tag_name':'find_elementS_by_tag_name'}
b_on_p_status=('enable','disable')