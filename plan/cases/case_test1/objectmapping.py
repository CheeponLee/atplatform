#! /usr/bin/env python
# -*- coding: utf-8 -*-
from objectmappingbase import search
from objectmappingbase import CheckedWebElement as we

driver=None
unionmon_login_username_1_web_element=None
unionmon_login_password_1_web_element=None
unionmon_login_submit_1_web_element=None

def gWebelement():
	global driver,unionmon_login_username_1_web_element,unionmon_login_password_1_web_element,unionmon_login_submit_1_web_element
	unionmon_login_username_1_web_element=we(driver,"web_element",["partial_link_text","eeeeeeeeee"])
