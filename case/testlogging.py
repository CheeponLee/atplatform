#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import logging
from  atplatform.case import sharedobject
def init():
	inituserlog()
	initadminlog()

def inituserlog():
	logger = logging.getLogger("selenium_user")
	filehandler = logging.FileHandler("./logs/userlog.log")
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
	filehandler = logging.FileHandler("./logs/adminlog.log")
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