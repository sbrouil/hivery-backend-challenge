import unittest
from backend.resources import data_utils

SIMPLE_PERSON = {
    "index": 0,
    "guid": "5e71dc5d-61c0-4f3b-8b92-d77310c7fa43",
    "has_died": True,
    "age": 61,
    "eyeColor": "blue",
    "name": "Carmella Lambert",
    "gender": "female",
    "company_id": 58,
    "friends": [],
    "favouriteFood": [
        "orange",
        "apple",
        "celery",
        "strawberry"
    ]
}

SIMPLE_COMPANY_MAP = {
    58: { 'index': 58, 'name': 'CORP' }
}

class TestLoadData(unittest.TestCase):
    def test_load_companies(self):
        companies = data_utils.load_companies()
        self.assertEqual(len(companies), 100)
    
    def test_load_people(self):
        people = data_utils.load_people()
        self.assertEqual(len(people), 1000)

    def test_people_food_vocabulary(self):
        people = [{
            'favouriteFood': ['apple', 'beans']
        }, {
            'favouriteFood': ['pineapple', 'carots']
        }]
        vocabulary = data_utils.people_food_vocabulary(people)
        self.assertSetEqual({'apple', 'beans', 'pineapple', 'carots'}, vocabulary)

    def test_every_food_from_people_file_has_category(self):
        people = data_utils.load_people()
        food = data_utils.people_food_vocabulary(people)
        for f in food:
            self.assertIn(data_utils.food_category(f), ['vegetable', 'fruit'], f + ' should have a category')

    def test_prepare_person_document_split_food_in_categories(self):
        document = data_utils.prepare_person_document(SIMPLE_PERSON, SIMPLE_COMPANY_MAP, {})
        self.assertDictEqual(document['favourite_food'], {
            'vegetables': ['celery'],
            'fruits': ['orange', 'apple', 'strawberry']
        })

    def test_prepare_person_document_rename_eye_color(self):
        document = data_utils.prepare_person_document(SIMPLE_PERSON, SIMPLE_COMPANY_MAP, {})
        self.assertFalse('eyeColor' in document)
        self.assertTrue('eye_color' in document)
        self.assertEqual(document['eye_color'], SIMPLE_PERSON['eyeColor'])
