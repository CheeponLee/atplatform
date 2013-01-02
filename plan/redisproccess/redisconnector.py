#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import redis
import atplatform.plan.commonparam as cp
pools=[]

def getpool(host='127.0.0.1',port=6379,db=0,_from=''):
	global pools
	if _from=='commonparam':
		host=cp.redisip
		port=cp.redisport
		db=cp.redisdefaultdb
	pool = redis.ConnectionPool(host=host, port=port, db=db)
	pools.append(pool)
	return pool

def getconnector(pool):
	r = redis.Redis(connection_pool=pool)
	return r

def closeallpools():
	global pools
	for i in pools:
		i.disconnect()
	return True
