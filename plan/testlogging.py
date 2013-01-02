#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import logging
from  atplatform.plan import sharedobject
def init(log_level):
	inituserlog(log_level)
	initadminlog(log_level)
	initrunmanagerlog(log_level)
	initplanprogresslog(log_level)
	initcaseexecuteerrorlog(log_level)

def inituserlog(log_level):
	logger = logging.getLogger("selenium_user")
	filehandler = logging.FileHandler("./logs/user.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)
	logger.addHandler(streamhandler)
	sharedobject.userlog=logger

def initadminlog(log_level):
	logger = logging.getLogger("selenium_admin")
	filehandler = logging.FileHandler("./logs/admin.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)  
	logger.addHandler(streamhandler)
	sharedobject.adminlog=logger

def initrunmanagerlog(log_level):
	logger = logging.getLogger("selenium_runmanager")
	filehandler = logging.FileHandler("./logs/runmanager.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)  
	logger.addHandler(streamhandler)
	sharedobject.runmanagerlog=logger

def initplanprogresslog(log_level):
	logger = logging.getLogger("selenium_planprogress")
	filehandler = logging.FileHandler("./logs/planprogress.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)  
	logger.addHandler(streamhandler)
	sharedobject.planprogresslog=logger

def initcaseexecuteerrorlog(log_level):
	logger = logging.getLogger("selenium_caseexecuteerror")
	filehandler = logging.FileHandler("./logs/caseexecuteerror.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)  
	logger.addHandler(streamhandler)
	sharedobject.caseexecuteerrorlog=logger

def shutdownlog():
	logging.shutdown()