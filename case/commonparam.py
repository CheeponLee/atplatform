#! /usr/bin/env python 
# -*- coding: utf-8 -*- 

uploadcaseport=778
tmpdir='tmp/'
casesdir='/home/uls/software/atplatform/plan/cases/'
maxuploadcase=20

# db
Connect_string='mysql+mysqldb://root:root@192.168.1.114:3306/selenium?charset=utf8'
dbpoolsize=50
dbpool_recycle=3600
dbpool_timeout=15
dbecho=False