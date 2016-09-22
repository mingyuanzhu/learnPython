#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def evaluation():

	extraConfig = {"aa":"aa"}

	param = {
		'description': 'test',
		'version': '3.1.0',
		'dataSetName': 'less data',
		'searchEndpoint': 'http://visearch.visenze.com',
		'adminEndpoint': 'http://visearch-admin.visenze.com',
		'accountId': 8,
		'appId': 1327,
		'isUseFq': True,
		'detect': 'all',
		'visearchCount': 10,
		'threadCount': 10,
		'extraConfig': str(extraConfig)
	}

	r = requests.post('http://localhost:8080/api/v1/experiment', auth = ('admin', 'evaluation_123'), data = param)

	print(r)

evaluation()