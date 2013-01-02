#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import logging
from  atplatform.report import sharedobject
def init(log_level):
	inituserlog(log_level)
	initadminlog(log_level)
	initprocesslog(log_level)

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

def initprocesslog(log_level):
	logger = logging.getLogger("selenium_process")
	filehandler = logging.FileHandler("./logs/process.log")
	streamhandler = logging.StreamHandler()
	fmt = logging.Formatter('[%(levelname)s]: %(asctime)s, %(funcName)s, %(message)s')
	filehandler.setFormatter(fmt)
	streamhandler.setFormatter(fmt)
	logger.setLevel(log_level)
	logger.addHandler(filehandler)
	logger.addHandler(streamhandler)
	sharedobject.processlog=logger

def shutdownlog():
	logging.shutdown()