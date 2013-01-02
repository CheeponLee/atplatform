#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import objectmappingbase as ombase
# loginname_='''find_element_by_name("tl_login")'''
# loginpass_='''find_element_by_name("tl_password")'''
# submit_='''find_element_by_name("login_submit")'''
# csgf_=u'''find_element_by_partial_link_text("测试规约")'''
# from selenium.webdriver.remote.webelement import WebElement

driver=None
q=None
submit=None

def gWebelement():
	global driver,q,submit
	q=ombase.search(driver,3)
	submit=ombase.search(driver,4)