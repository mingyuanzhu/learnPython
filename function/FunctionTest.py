#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# return the two answer
# ax2 + bx + c = 0
# x=(-b±√(b^2-4ac))/2a
import math

def quadratic(a, b, c):
	if a == 0 and c == 0:
		return 0
	elif a == 0 and b == 0:
		return 'error'
	elif a == 0:
		return c/b;
	else:
		return (-b + math.sqrt(b**2 - 4*a*c)) / (2 * a), (-b - math.sqrt(b**2 - 4*a*c)) / (2 * a)

print('2x^2 + 3x + 1 = 0 ==> ' , quadratic(2, 3, 1))
print('x^2 + 3x - 4 = 0 ==> ' , quadratic(1, 3, -4))