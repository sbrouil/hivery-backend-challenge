import unittest
from backend import create_app
from backend.tests import RestTest
from backend.db import get_db

GUID_TEST = 'a2e80b74-eaec-4b1a-a3e9-f71b850332a5'
NON_NEXISTANT_UUID = 'd9cdbbda-c13c-488d-8d5b-c9a3aaf5d1f7'
INVALID_UUID = 'hh5e71dc5d-61c0-4f3b-8b92-d77310c7fa43hhh'
TECH_ID = '595eeb9b96d80a5bc7afb106'

FRIEND_0 = {
    'guid' : '5e71dc5d-61c0-4f3b-8b92-d77310c7fa43',
    'index' : 0,
    'has_died' : True,
    'eye_color' : 'blue',
    'name' : 'Carmella Lambert',
    'gender' : 'female'
}

FRIEND_1 = {
    'guid' : 'b057bb65-e335-450e-b6d2-d4cc859ff6cc',
    'index' : 1,
    'has_died' : False,
    'eye_color' : 'brown',
    'name' : 'Decker Mckenzie',
    'gender' : 'male'
}

FRIEND_2 = {
    'guid' : '49c04b8d-0a96-4319-b310-d6aa8269adca',
    'index' : 2,
    'has_died' : False,
    'eye_color' : 'blue',
    'name' : 'Bonnie Bass',
    'gender' : 'female'
}

FRIEND_3 = {
    'guid' : 'c51b3deb-7b93-43da-b36d-4804d256080c',
    'index' : 3,
    'has_died' : False,
    'eye_color' : 'brown',
    'name' : 'Harris Sailor',
    'gender' : 'male'
}

FRIEND_4 = {
    'guid' : 'ef9fc111-af7f-4f27-93b4-e6cd67e35ac0',
    'index' : 4,
    'has_died' : False,
    'eye_color' : 'brown',
    'name' : 'Pascale Sailor',
    'gender' : 'female',
}

JULIA = {
    'guid' : 'a5c37a3d-3e0d-4aba-adc5-51cf83283611',
    'name': 'Julia Woberts',
    'age': 51,
    'address': '7421 Whitsett ave',
    'phone': '1 987 877 876',
    'email': 'julia.woberts@gmail.par',
    'friends': [FRIEND_0, FRIEND_1, FRIEND_2, FRIEND_3]
}

JENNY = {
    'guid' : '4848224f-aab9-4123-b331-69114316150e',
    'name': 'Jenny Laurence',
    'age': 28,
    'address': '7737 Bell ave',
    'phone': '1 987 877 876',
    'email': 'jenny.laurence@gmail.par',
    'friends': [FRIEND_0, FRIEND_1, FRIEND_2, FRIEND_4]
}

class PeopleIntegrationTest(RestTest):

    # GET /v1/people/:id

    PEOPLE_DETAIL_ENDPOINT = '/v1/people/%s'

    def test_get_person(self):
        self.db.people.insert_one({
            '_id': TECH_ID,
            'guid': GUID_TEST,
            'name': 'Test User' 
        })

        response = self.client.get(self.PEOPLE_DETAIL_ENDPOINT % GUID_TEST)
        data = response.get_json()
        self.assertDictEqual(data, {
            '_id': TECH_ID,
            'guid': GUID_TEST,
            'name': 'Test User' 
        })

    def test_get_person_with_invalid_uuid_returns_400(self):
        response = self.client.get(self.PEOPLE_DETAIL_ENDPOINT % INVALID_UUID)
        data = response.get_json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The given UUID is invalid: badly formed hexadecimal UUID string')

    def test_get_nonexistant_person_returns_404(self):
        response = self.client.get(self.PEOPLE_DETAIL_ENDPOINT % NON_NEXISTANT_UUID)
        data = response.get_json()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)

    # GET /v1/people/:id/favourite-food
    
    PEOPLE_FAVOURITE_FOOD_ENDPOINT = PEOPLE_DETAIL_ENDPOINT + '/favourite-food'

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

        response = self.client.get(self.PEOPLE_FAVOURITE_FOOD_ENDPOINT % GUID_TEST)
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
        self.assertEqual(response.status_code, 404)

        data = response.get_json()
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)

    # GET /v1/people/:guid_source/mutual-friends/guid_target

    MUTUAL_FRIENDS_ENDPOINT = '/v1/people/%s/mutual-friends/%s'

    def test_get_mutual_friends_should_return_source_information(self):
        self.db.people.insert_one(JULIA)
        self.db.people.insert_one(JENNY)

        response = self.client.get(self.MUTUAL_FRIENDS_ENDPOINT % (JULIA['guid'], JENNY['guid']))
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        self.assertDictEqual(data['source'], {
            'name': JULIA['name'],
            'age': JULIA['age'],
            'address': JULIA['address'],
            'phone': JULIA['phone']
        })

    def test_get_mutual_friends_should_return_target_information(self):
        self.db.people.insert_one(JULIA)
        self.db.people.insert_one(JENNY)

        response = self.client.get(self.MUTUAL_FRIENDS_ENDPOINT % (JULIA['guid'], JENNY['guid']))
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        self.assertDictEqual(data['target'], {
            'name': JENNY['name'],
            'age': JENNY['age'],
            'address': JENNY['address'],
            'phone': JENNY['phone']
        })

    def test_get_mutual_friend_should_return_friends_in_common(self):
        self.db.people.insert_one(JULIA)
        self.db.people.insert_one(JENNY)

        response = self.client.get(self.MUTUAL_FRIENDS_ENDPOINT % (JULIA['guid'], JENNY['guid']))
        self.assertEqual(response.status_code, 200)
        
        data = response.get_json()
        expected_friends = set([FRIEND_0['guid'], FRIEND_1['guid'], FRIEND_2['guid']])
        actual_friends = set(map(lambda f: f['guid'], data['mutual_friends']))
        self.assertSetEqual(actual_friends, expected_friends)

    def test_get_mutual_friend_should_match_filters(self):
        self.db.people.insert_one(JULIA)
        self.db.people.insert_one(JENNY)

        # only FRIEND_1, FRIEND_3, FRIEND_4 have these criteria, but only FRIEND_1 is is common
        response = self.client.get((self.MUTUAL_FRIENDS_ENDPOINT + '?eye_color=brown&has_died=false') % (JULIA['guid'], JENNY['guid']))
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        expected_friends = [FRIEND_1['guid']]
        actual_friends = list(map(lambda f: f['guid'], data['mutual_friends']))
        self.assertListEqual(actual_friends, expected_friends)
    
    def test_get_mutual_friend_should_return_empty_friend_list(self):
        self.db.people.insert_one(JULIA)
        self.db.people.insert_one(JENNY)

        # no common friend is died with brown eye
        response = self.client.get((self.MUTUAL_FRIENDS_ENDPOINT + '?eye_color=brown&has_died=true') % (JULIA['guid'], JENNY['guid']))
        self.assertEqual(response.status_code, 200)

        data = response.get_json()
        expected_friends = []
        actual_friends = list(map(lambda f: f['guid'], data['mutual_friends']))
        self.assertListEqual(actual_friends, expected_friends)

    def test_get_mutual_friend_with_first_person_nonexistant_should_return_404(self):
        self.db.people.insert_one(JENNY)

        response = self.client.get(self.MUTUAL_FRIENDS_ENDPOINT % (NON_NEXISTANT_UUID, JENNY['guid']))
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)

    def test_get_mutual_friend_with_second_person_nonexistant_should_return_404(self):
        self.db.people.insert_one(JULIA)

        response = self.client.get(self.MUTUAL_FRIENDS_ENDPOINT % (JULIA['guid'], NON_NEXISTANT_UUID))
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['message'], 'Person %s not found' % NON_NEXISTANT_UUID)