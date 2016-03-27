#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import reduce

def prod(L):

	def multiple(x, y):
		return x * y
	return reduce(multiple, L)

print('3 * 5 * 7 * 9 =', prod([3, 5, 7, 9]))