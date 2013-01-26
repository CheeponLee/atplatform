#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import logging
from  atplatform.case import sharedobject
import os
from  atplatform.case import commonparam as cp

def init():
	inituserlog()
	initadminlog()

def inituserlog():
	logger = logging.getLogger("selenium_user")
	touchfile(cp.home+"logs/user.log")
	filehandler = logging.FileHandler(cp.home+"logs/user.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(filehandler)
	logger.addHandler(streamhandler)
	sharedobject.userlog=logger

def initadminlog():
	logger = logging.getLogger("selenium_admin")
	touchfile(cp.home+"logs/admin.log")
	filehandler = logging.FileHandler(cp.home+"logs/admin.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(filehandler)  
	logger.addHandler(streamhandler)
	sharedobject.adminlog=logger

def shutdownlog():
	logging.shutdown()

def touchfile(filename):
	if not os.path.exists(filename):
		file(filename,'w').close()
