#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def multiplication(x, y):
	return lambda x,y: x * y

f = multiplication(2, 5)

print(f(2, 5))
print(f())