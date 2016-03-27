#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import functools

def log():
	@functools.wraps(func)
	def wrapper(*args, **kw):
		print('call method %s()' % func.__name__)
		return func(*args, **kw)
	return wrapper

def log2(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('%s call method %s()' % (text, func.__name__))
			return func(*args, **kw)
		return wrapper
	return decorator

def log3(text):
	if isinstance(text, (str, int, float)):
		def decorator(func):
			@functools.wraps(func)
			def wrapper(*args, **kw):
				print('%s call method %s()' % (text, func.__name__))
				return func(*args, **kw)
			return wrapper
		return decorator
	else:
		func = text
		@functools.wraps(func)
		def wrapper(*args, **kw):
			print('call method %s()' % func.__name__)
			return func(*args, **kw)
		return wrapper

@log3
def now():
	print('2016-03-27')

@log3('text context')
def now2():
	print('2016-03-27')

now()
now2()
print(now.__name__)
print(now2.__name__)