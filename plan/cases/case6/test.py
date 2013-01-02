#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import objectmapping as om
from case2 import testcase
from selenium import webdriver
config={'Webdriverhub': 'http://localhost:4444/wd/hub', 'Browserversion': '9', 'Javascriptenabled': 'True', 'ignoreProtectedModeSettings': True, 'Platform': 'WINDOWS', 'Browsername': 'IE', 'Findtimeout': 15}
a=testcase(config)
a.driver=webdriver.Chrome()
om.driver=a.driver
om.gWebelement()

a.before()
a.action()
a.clean()