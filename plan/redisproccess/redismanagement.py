#! /usr/bin/env python 
# -*- coding: utf-8 -*- 
import redis
import time

host=None
port=None
client=None
heartbeattime=10

def init(_host='127.0.0.1',_port=6379,db=0):
	global client,host,port
	host=_host
	port=_port
	client=redis.StrictRedis(host=_host, port=_port, db=db)

def close():
	host=None
	port=None
	client=None

def heartbeat():
	global client,heartbeattime
	client=r.ping()
	if re!=True:
		raise Exception('redis cannot be reached.')
	times.sleep(heartbeattime)

def get_dbsize(db=0):
	global host,port
	client=redis.StrictRedis(host=host, port=port, db=db)
	try:
		size=client.dbsize()
	except Exception,e:
		raise e
	finally:
		del client
	return size

def get_info():
	global client
	return client.info()	#return a dict

def config_get(key):
	return client.config_get(key)

def config_set(key,value):
	return client.config_set(key,value)	#return True or False

def debug_object(key):
	return client.debug_object(key)		#return a dict

def flush_all():
	return client.flush_all()

def flush_db(db=0):
	return client.flush_db(db)

def save():
	client.save()	#save to disk