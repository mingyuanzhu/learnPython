#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a student object'

__author__ = 'mingyuan'

class Student(object):
	"""docstring for ClassName"""
	def __init__(self, name, score):
		super(object, self).__init__()
		self.__name = name
		self.__score = score

	def printinfo(self):
		print("Strudent info: %s, %s" % (self.__name, self.__score))

student = Student('tom', '60')

student.printinfo()