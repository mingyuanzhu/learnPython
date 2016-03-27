#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

def str2float(s):

	def numfilter(c):
		num = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '.': None}[c]
		if num != None:
			return num

	def floatDigit(s):
		nums = s.split('.')
		if len(nums) == 2:
			return len(nums[1])
		else:
			return 0.1

	def fn(x, y):
		if y == None:
			return x
		else:
			return x * 10 + y;

	return reduce(fn, map(numfilter, s)) / 10**floatDigit(s);

print('str2float(\'123.456\') =', str2float('123.456'))