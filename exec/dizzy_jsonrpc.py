#!/usr/bin/env python

import requests
import json
import random

class JSONRPC(object):
	 headers = {'content-type': 'application/json'}

	 def __init__(self, url):
	 	self.url = url

	 def execute(self, function, params):
	 	payload = { "method": function,
        			"params": params,
        			"jsonrpc": "2.0",
        			"id": random.randrange(0, 10000000000)}
		response = requests.post(self.url, data=json.dumps(payload), headers=self.headers).json()
		return response

