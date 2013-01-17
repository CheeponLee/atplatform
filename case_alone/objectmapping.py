#! /usr/bin/env python
# -*- coding: utf-8 -*-
try:
	from atplatform.plan.objectmappingbase import search
except:
	from objectmappingbase import search
try:
	from atplatform.plan.objectmappingbase import CheckedWebElement as we
except:
	from objectmappingbase import CheckedWebElement as we

driver=None
unionmon_login_username_2_web_element=None

def gWebelement():
	global driver,unionmon_login_username_2_web_element
	unionmon_login_username_2_web_element=search(driver,29,2091)

