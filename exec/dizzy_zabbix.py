#!/usr/bin/env python

import requests
import json
import random
import re

class Zabbix(object):
	 headers = {'content-type': 'application/json'}

	 def __init__(self, url, user, password):
	 	api_path = '/api_jsonrpc.php' 
	 	self.url = url + api_path if not re.search('%s$' % api_path, url) else url
	 	self.user = user
	 	self.password = password
	 	self.token = self.login(self.user, self.password)

	 def x(self, function, params):
	 	payload = { "method": function,
        			"params": params,
        			"auth": self.token,
        			"jsonrpc": "2.0",
        			"id": random.randrange(0, 1000000)}
		response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
		try:
			return response['result']
		except KeyError:
			return response['error']

	 def login(self, user, password):
	 	payload = { "method": 'user.login',
        			"params": {'user':user, 'password':password},
        			"jsonrpc": "2.0",
        			"id": random.randrange(0, 1000000)}
		response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
		try:
			return response['result']
		except KeyError:
			raise Exception(response['error'])
