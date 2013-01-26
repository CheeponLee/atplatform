#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import logging
from  atplatform.plan import sharedobject
import os
from  atplatform.plan import commonparam as cp

def init(log_level):
	inituserlog(log_level)
	initadminlog(log_level)
	initrunmanagerlog(log_level)
	initplanprogresslog(log_level)
	initcaseexecuteerrorlog(log_level)

def inituserlog(log_level):
	logger = logging.getLogger("selenium_user")
	touchfile(cp.home+"logs/user.log")
	filehandler = logging.FileHandler(cp.home+"logs/user.log")
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
	touchfile(cp.home+"logs/admin.log")
	filehandler = logging.FileHandler(cp.home+"logs/admin.log")
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
	touchfile(cp.home+"logs/runmanager.log")
	filehandler = logging.FileHandler(cp.home+"logs/runmanager.log")
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
	touchfile(cp.home+"logs/planprogress.log")
	filehandler = logging.FileHandler(cp.home+"logs/planprogress.log")
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
	touchfile(cp.home+"logs/caseexecuteerror.log")
	filehandler = logging.FileHandler(cp.home+"logs/caseexecuteerror.log")
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

def touchfile(filename):
	if not os.path.exists(filename):
		file(filename,'w').close()