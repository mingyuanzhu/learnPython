#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def is_palindrome(n):
	string = str(n)
	length = len(string)
	leftIndex = 0
	rightIndex = 0
	#odd
	if length % 2:
		leftIndex = length // 2 - 1
		rightIndex = length // 2 + 1
	else:
		leftIndex = length // 2 - 1
		rightIndex = length // 2
	while leftIndex >= 0 and rightIndex < length:
		if string[leftIndex] != string[rightIndex]:
			return False
		else:
			leftIndex -= 1
			rightIndex -= 1
	return True

output = filter(is_palindrome, range(1, 1000))
print(list(output))