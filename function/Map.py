#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def normalize(name):
	return ''.join([c.lower() if index else c.upper() for index,c in enumerate(name)])

L1 = ['adam', 'LISA', 'barT']
L2 = list(map(normalize, L1))
print(L2)