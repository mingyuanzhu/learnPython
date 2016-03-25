#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import Iterable

print('======iterator string=====')
string = 'string'
if isinstance(string, Iterable):
	for c in string:
		print(c)

print('======iterator list with index')
l = ['aa', 'bb', 'cc']
for index, value in enumerate(l):
	print('index: ', index, ' value: ', value)

print('======iterator dict======')
d = {'jordan': 23, 'kobe': 24, 'curry': 30}
for key in d:
	print('key: ', key, ' value: ', d[key])

for value in d.values():
	print('value: ', value)

for k, v in d.items():
	print('key: ', k, ' value: ', v)