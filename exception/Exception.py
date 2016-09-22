#!/usr/bin/env python3
#! -*- coding:utf-8 -*-

import logging

logging.basicConfig(level=logging.INFO)

def test_raise():
	raise ValueError('value error test')

def catch_exception():
	try:
		test_raise()
	except ValueError as e:
		logging.exception(e)
	finally:
		logging.info("error")

catch_exception()