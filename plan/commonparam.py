#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
home='/home/uls/workplace/atplatform/atplatform/plan/'
exceptionpicdir='/home/uls/workplace/atplatform/atplatform/exceptionpic/'
exctmpdir = '/home/uls/workplace/atplatform/atplatform/plan/exctmp/'
mqhost="localhost"
maxpush=5
maxconcurrent=2
acutlibhost='127.0.0.1:774'
defaultweight=10   #0<=x<=1,000,000
maxconcurrentplan=9
restricteduserid=1002

#redis
redisip='127.0.0.1'
redisport=6379
redisdefaultdb=1

# db
Connect_string='mysql+mysqldb://root:root@127.0.0.1:3306/selenium?charset=utf8'
dbpoolsize=50
dbpool_recycle=3600
dbpool_timeout=15
dbecho=False