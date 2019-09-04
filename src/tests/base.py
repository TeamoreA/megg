import json
from django.test import TestCase
from graphene.test import  Client
from megg.schema import schema

from users.models import CustomUser


class BaseTestCase(TestCase):
    """Base class for setting up tests"""
    def setUp(self):
        """Initialize the test client"""
        self._client = Client(schema)

        user1 = CustomUser(
            username="Tim",
            email="tim@app.com",
            password="Teamore123",
            first_name="Timothy",
            last_name="Kamau")
        user1.save()

    def query(self, query: str):
        """Perform tests queries"""
        executed = self._client.execute(query)                        
        json_resp = json.loads(json.dumps(executed))
        return json_resp

    def assertResponseNoErrors(self, resp: dict, expected: dict):
        '''
        Assert response
        '''
        self.assertNotIn('errors', resp, 'Response had errors')
        self.assertEqual(resp, expected, 'Response has correct data')
  
