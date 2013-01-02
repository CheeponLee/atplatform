#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
import objectmapping as om
from testcasebase import testcasebase

class testcase(testcasebase):

	def __init__(self,config,queue):
		testcasebase.__init__(self,config,queue)

	def init(self):
		#driver=eval('webdriver.'+self.browsername+'()')
		testcasebase.init(self)
		om.driver=self.driver
		om.gWebelement()

	def before(self):
		super(testcase,self).before()
		pass

	def action(self):
		om.driver.get('http://www.baidu.com')
		om.q.send_keys('testlink')
		om.submit.submit()
		time.sleep(5)
		t=om.driver.page_source.find(u"testlink")
		if t<0:
			raise Exception("ËÑË÷½á¹û´íÎó")

	def clean(self):
		super(testcase,self).clean()
		om.driver.quit()

# Create a new instance of the Firefox driver
# driver = webdriver.Firefox()

# # go to the google home page
# driver.get("http://www.google.com")
# driver.implicitly_wait(10)
# # find the element that's name attribute is q (the google search box)
# inputElement = driver.find_element_by_name("q")

# # type in the search
# inputElement.send_keys("Cheese!")

# # submit the form (although google automatically searches now without submitting)
# inputElement.submit()

# # the page is ajaxy so the title is originally this:
# print driver.title

# try:
#     # we have to wait for the page to refresh, the last thing that seems to be updated is the title
#     WebDriverWait(driver, 10).until(lambda driver : driver.title.lower().startswith("cheese!"))

#     # You should see "cheese! - Google Search"
#     print driver.title

# finally:
#     driver.quit()

if __name__=='__main__':
	config={'Webdriverhub': 'http://localhost:4444/wd/hub', 'Browserversion': '9', 'Javascriptenabled': 'True', 'ignoreProtectedModeSettings': True, 'Platform': 'WINDOWS', 'Browsername': 'IE', 'Findtimeout': 15}
	a=testcase(config)
	a.driver=webdriver.Chrome()
	om.driver=a.driver
	om.gWebelement()

	a.before()
	a.action()
	a.clean()
