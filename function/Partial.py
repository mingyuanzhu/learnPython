#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

print('12345 convert %s ' % int('12345'))

int2 = functools.partial(int, base = 2)

print('11111111 convert %s ' % int2('11111111'))