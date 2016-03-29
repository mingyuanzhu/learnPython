#/usr/bin/env python3
# -*- coding: utf-8 -*-

' module base knowledge '

__author__ = 'zhumingyuan'

import sys

def hello():
	# get cmd input args
	args = sys.argv
	if len(args) == 1:
		print('hello world')
	elif len(args) == 2:
		print('hello %s' % args[1])
	else:
		print('too many args')

if __name__ == '__main__':
	hello()
