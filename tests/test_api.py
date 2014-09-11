#!/usr/bin/python
#-*- coding: utf-8 -*-
import requests
import json

new_android_user = {'id': '1337', 'reg_id': '1234', 'category': 'simpleuser', 'extra_info': 'android 5.0 samsung galaxy s6 etc.'}
r = requests.post('http://dela.bg:1234/api/v1/androidusers', data=json.dumps(new_android_user), headers={'content-type': 'application/json', 'authorization': 'mysecretauthkey'})

if r.status_code != 201:
    print("API POST FAILED >> status code: " + str(r.status_code))
else:
    print("POST ... ok")



