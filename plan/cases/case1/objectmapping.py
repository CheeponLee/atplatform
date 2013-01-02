#! /usr/bin/env python
# -*- coding: utf-8 -*-
from objectmappingbase import CheckedWebElement as we

driver=None
zhidao_1_web_element=None

def gWebelement():
	global driver,zhidao_1_web_element
	zhidao_1_web_element=we(driver,'web_element',['name','tj_zhidao'])

