import unittest
from backend import create_app
from backend.db import get_db

GUID_TEST = 'a2e80b74-eaec-4b1a-a3e9-f71b850332a5'
TECH_ID = '595eeb9b96d80a5bc7afb106'

class PeopleIntegrationTest(unittest.TestCase):
    """ Test the /people API endpoint
    """
    def setUp(self):
        self.app = create_app({
            'mongodb': {
                'host': 'localhost',
                'port': 27017,
                'database': 'hivery_integration_test'
            }
        })
        self.client = self.app.test_client()    
        with self.app.app_context():
            self.db = get_db()
            # erase all existing data to ensure tests are independant
            self.db.people.drop()
        
    def test_get_person(self):
        self.db.people.insert_one({
            '_id': TECH_ID,
            'guid': GUID_TEST,
            'name': 'Test User' 
        })

        response = self.client.get('/v1/people/%s' % GUID_TEST)
        data = response.get_json()
        self.assertDictEqual(data, {
            '_id': TECH_ID,
            'guid': GUID_TEST,
            'name': 'Test User' 
        })
    
    def test_get_person_favourite_food(self):
        self.db.people.insert_one({
            '_id' : TECH_ID,
            'guid' : GUID_TEST,
            'age' : 61,
            'name': 'Carmella Lambert',
            'gender' : 'female',
            'email' : 'carmellalambert@earthmark.com',
            'favourite_food' : {
                'fruits': [
                    'orange',
                    'apple',
                    'banana'
                ],
                'vegetables': [
                    'celery'
                ]
            }
        })

        response = self.client.get('/v1/people/%s/favourite-food' % GUID_TEST)
        data = response.get_json()
        self.assertDictEqual(data, {
            'username': 'Carmella Lambert',
            'age': 61,
            'fruits': [
                'orange',
                'apple',
                'banana'
            ],
            'vegetables': [
                'celery'
            ]
        })
