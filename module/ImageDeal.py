#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' test import the image deal module '

__author__ = 'mingyuan'

from PIL import Image

im = Image.open('/Users/zhumingyuan/Downloads/1df1a352b5ed6694b9b51c5f223dc0a0e11d8562.jpg')
print(im.format, im.size, im.mode)

im.thumbnail((100,147))
im.save('/Users/zhumingyuan/Downloads/press.png', 'PNG')