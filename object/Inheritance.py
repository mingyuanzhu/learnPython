#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' object inherite and duck modle '

__author__ = 'mingyuan'

class Animal(object):
	def run(self):
		print('animal is running ...')

# Dog inherite Animal
class Dog(Animal):
	"""docstring for Dog"""

	def run(self):
		print('dog is running ...')

# duck model
class Duck(object):
	"""docstring for duck"""
	
	def run(self):
		print('duck is running ...')

def animal_run(animal):
	animal.run()

animal_run(Animal())
animal_run(Dog())
animal_run(Duck())

		