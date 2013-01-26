#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
home='/home/uls/workplace/atplatform/atplatform/case/'
uploadcaseport=778
tmpdir = home+'tmp/'
casesdir='/home/uls/workplace/atplatform/atplatform/plan/cases/'
maxuploadcase=20

# db
Connect_string='mysql+mysqldb://root:root@127.0.0.1:3306/selenium?charset=utf8'
dbpoolsize=50
dbpool_recycle=3600
dbpool_timeout=15
dbecho=False