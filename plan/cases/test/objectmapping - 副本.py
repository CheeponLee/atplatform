#! /usr/bin/env python
# -*- coding: utf-8 -*-
from objectmappingbase import CheckedWebElement as we
from objectmappingbase import search

driver=None
unionmon_login_username_1_web_element=None
unionmon_login_password_1_web_element=None
unionmon_login_submit_1_web_element=None

def gWebelement():
	global driver,unionmon_login_username_1_web_element,unionmon_login_password_1_web_element,unionmon_login_submit_1_web_element
	unionmon_login_username_1_web_element=we(driver,web_element,[css_selector,qqq1111])
	unionmon_login_password_1_web_element=search(driver,27,2090)
	unionmon_login_submit_1_web_element=search(driver,28,2092)
