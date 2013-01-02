#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import objectmappingbase as ombase
# loginname_='''find_element_by_name("tl_login")'''
# loginpass_='''find_element_by_name("tl_password")'''
# submit_='''find_element_by_name("login_submit")'''
# csgf_=u'''find_element_by_partial_link_text("测试规约")'''
# from selenium.webdriver.remote.webelement import WebElement

driver=None
loginname=None
loginpass=None
submit=None
csgf=None

def gWebelement():
	global driver,loginname,loginpass,submit,csgf
	loginname=ombase.search(driver,231)
	loginpass=ombase.search(driver,231)
	submit=ombase.search(driver,231)
	csgf=ombase.search(driver,231)
