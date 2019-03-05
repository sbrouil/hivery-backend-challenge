import unittest
from backend import create_app

class PeopleIntegrationTest(unittest.TestCase):
    """ Test the /people API endpoint
    """
    def setUp(self):
        app = create_app()
        self.client = app.test_client()        
        
    def test_get_person(self):
        response = self.client.get('/v1/people/person1')
        data = response.get_json()
        self.assertDictEqual(data, {'name': 'person'})
