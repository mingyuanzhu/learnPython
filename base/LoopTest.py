#!/usr/bin/env python3
# -*- coding: utf-8 -*-
L = ['Bart', 'Lisa', 'Adam']
print('***** use for loop *****')
for name in L:
    print('Hello %s!' % name)

print('***** use while loop *****')
index = 0
while index < len(L):
    print('Hello %s!' % L[index])
    index += 1