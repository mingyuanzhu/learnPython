#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def triangles(n):
	l = []
	i = 0
	print(n)
	while i < n:
		if i == 0:
			l = [1]
			yield l
		else:
			new = [1]
			for index, v in enumerate(l):
				if index == len(l) - 1:
					new.append(1)
				else:
					new.append(l[index] + l[index + 1])
			l = new
			yield l
		i += 1

for item in triangles(10):
	print(item)