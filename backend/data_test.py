import unittest
import data

class TestLoadData(unittest.TestCase):
    def test_load_companies(self):
        companies = data.load_companies()
        self.assertEqual(len(companies), 100)
    
    def test_load_people(self):
        people = data.load_people()
        self.assertEqual(len(people), 1000)

    def test_people_food_vocabulary(self):
        people = [{
            'favouriteFood': ['apple', 'beans']
        }, {
            'favouriteFood': ['pineapple', 'carots']
        }]
        vocabulary = data.people_food_vocabulary(people)
        self.assertSetEqual({'apple', 'beans', 'pineapple', 'carots'}, vocabulary)

    def test_every_food_from_people_file_has_category(self):
        people = data.load_people()
        food = data.people_food_vocabulary(people)
        for f in food:
            self.assertIn(data.food_category(f), ['vegetable', 'fruit'], f + ' should have a category')
