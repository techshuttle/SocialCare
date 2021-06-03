import logging

import pytest
#
import logging
import unittest

import requests

LOG_LEVEL = logging.INFO
common_formatter = logging.Formatter('%(asctime)s [%(levelname)-7s][ln-%(lineno)-3d]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

BASE_URL = "http://127.0.0.1:5000/"

GET_URLS = "/get_urls"
ADD_SENTIMENT = "/add_sentiment"
ADD_MEMBERS = "/add_members"
GET_MEMBERS = "/get_members"
NOTIFY = "/notify"


class test_api_homepage(unittest.TestCase):
    def test_1_status_code(self):
        r = requests.get(BASE_URL)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        response = requests.get(BASE_URL)
        response_body = response.json()
        assert response_body["Result"] == "Success"

class test_get_urls(unittest.TestCase):

    def test_1_status_code(self):
        r = requests.get(BASE_URL + GET_URLS)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        pass



class test_add_sentiments(unittest.TestCase):
    def test_1_status_code(self):
        r = requests.post(BASE_URL + ADD_SENTIMENT)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        r = requests.post(BASE_URL + ADD_SENTIMENT)
        self.assertEqual(len(r.json()), 1)

class test_add_members(unittest.TestCase):
    def test_1_status_code(self):
        r = requests.post(BASE_URL + ADD_MEMBERS)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        pass



class test_get_members(unittest.TestCase):
    def test_1_status_code(self):
        r = requests.post(BASE_URL + GET_MEMBERS)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        pass

class test_notify(unittest.TestCase):
    def test_1_status_code(self):
        r = requests.get(BASE_URL + NOTIFY)
        self.assertEqual(r.status_code, 200)

    def test_2(self):
        pass
