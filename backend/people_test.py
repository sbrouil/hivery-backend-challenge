import unittest
from backend import create_app
from backend.tests import RestTest
from backend.db import get_db

GUID_TEST = 'a2e80b74-eaec-4b1a-a3e9-f71b850332a5'
NON_NEXISTANT_UUID = 'd9cdbbda-c13c-488d-8d5b-c9a3aaf5d1f7'
INVALID_UUID = 'hh5e71dc5d-61c0-4f3b-8b92-d77310c7fa43hhh'
TECH_ID = '595eeb9b96d80a5bc7afb106'

class PeopleIntegrationTest(RestTest):

    # GET /v1/people/:id

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

    def test_get_person_with_invalid_uuid_returns_400(self):
        response = self.client.get('/v1/people/%s' % INVALID_UUID)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The given UUID is invalid: badly formed hexadecimal UUID string')

    def test_get_nonexistant_person_returns_404(self):
        response = self.client.get('/v1/people/%s' % NON_NEXISTANT_UUID)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)

    # GET /v1/people/:id/favourite-food
    
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

    def test_get_nonexistant_person_favourite_food_returns_404(self):
        response = self.client.get('/v1/people/%s/favourite-food' % NON_NEXISTANT_UUID)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)