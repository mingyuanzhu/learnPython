#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def move(n, a = 'A', b = 'B', c = 'C'):
	if n == 1:
		formatPrint(a, c)
	else:
		move(n-1, a, c, b)
		formatPrint(a, c)
		move(n-1, b, a, c)

def formatPrint(f,t):
	print('move', f, '====>', t)

print('n = 3')
move(3)
print('==================')
print('n = 4')
move(4)
print('==================')
print('n = 5')
move(32)
