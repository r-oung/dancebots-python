#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

"""
{
	"move": {
		"type": "Forward",
		"fields": {
			"time": "5"
		}
	}
},
{
	"move": {
		"type": "Backward",
		"fields": {
			"time": "5"
		}
	}
},
{
	"turn": {
		"type": "Left",
		"fields": {
			"time": "5"
			"direction": "Forward"
		}
	}
},
{
	"turn": {
		"type": "Right",
		"fields": {
			"time": "5"
			"direction": "Backward"
		}
	}
},
"""

def forward(time):
	return [{'forward': time}]

def backward(time):
	return [{'backward': time}]

def backandforth(freq):
	return [{'backandforth': freq}]