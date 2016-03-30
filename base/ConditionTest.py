#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 低于18.5：过轻
# 18.5-25：正常
# 25-28：过重
# 28-32：肥胖
# 高于32：严重肥胖
height = 1.75
weight = 80.5
bmi = weight/height**2
if bmi < 18.5:
    print('Underweight')
elif bmi <= 25:
    print('Normal')
elif bmi <=28:
    print('Overweight')
elif bmi <=32:
    print('Obese')
else:
    print('Serverly Obese')