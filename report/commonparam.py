#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
mqhost="localhost"
exceptionpiclocation="C:\\workplace\\exceptionpic\\"
reporthome="C:\\workplace\\atplatform\\report\\"
resultslocation=reporthome+"static\\results\\"
resultstmplocation=reporthome+"temp\\"
basereportlocation=reporthome+"basereport\\"

# db
Connect_string='mysql+mysqldb://root:root@127.0.0.1:3306/selenium?charset=utf8'
dbpoolsize=50
dbpool_recycle=3600
dbpool_timeout=15
dbecho=True