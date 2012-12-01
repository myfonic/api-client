import unittest
import os
import sys
sys.path.append(os.path.abspath("../client"))
import client
import requests

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.apiKey = "7d68e77942ad683609d7da601a24c8ae33a36f94" #testapi1 api-key
        self.client = client.RestApiClient(apiKey = self.apiKey)
        
    def assertStatusCode(self, response, expectedCode):
        self.assertEqual(response[0], expectedCode, \
                         "Unexpected status code received")
        
    def assertStatusOk(self, response):
        self.assertStatusCode(response, requests.codes["ok"])
        
    def assertFonic(self, fonic, fonicType, author, title, description, isPublic):
        self.assertEqual(fonic["type"], fonicType)
        self.assertEqual(fonic["author"], author)
        self.assertEqual(fonic["title"], title)
        self.assertEqual(fonic["fonic_description"], description)
        self.assertEqual(fonic["visibility"], str(int(isPublic)))