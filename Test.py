import unittest

import json
import urllib.request as urllib2


class TestViews(unittest.TestCase):
    def test_register(self):
        input_data = str(json.dumps({'username' : "max", 'password' : "123"})).encode('utf-8')
        req = urllib2.Request('http://127.0.0.1:5000/register', data = input_data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        data = json.load(resp)
        assert data == 'Successful'
    def test_getProfessor(self):
        input_data = str(json.dumps({'username' : "max", 'password' : "123"})).encode('utf-8')
        req = urllib2.Request('http://127.0.0.1:5000/getProfessor', data = input_data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        data = json.load(resp)
        assert data == 'Successful'
    def test_add_course(self):
        input_data = str(json.dumps({'username' : "max", 'password' : "123"})).encode('utf-8')
        req = urllib2.Request('http://127.0.0.1:5000/add_course', data = input_data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        data = json.load(resp)
        assert data == 'Successful'
    def test_add_professor(self):
        input_data = str(json.dumps({'username' : "max", 'password' : "123"})).encode('utf-8')
        req = urllib2.Request('http://127.0.0.1:5000/add_professor', data = input_data)
        req.add_header('Content-Type', 'application/json')
        resp = urllib2.urlopen(req)
        data = json.load(resp)
        assert data == 'Successful'
