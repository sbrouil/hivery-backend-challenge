import json
import os
import itertools
import copy

RESOURCE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/resources'

FRUIT = 'fruit'
VEGETABLE = 'vegetable'
FOOD_CATEGORY = {
    'beetroot': VEGETABLE,
    'banana': FRUIT,
    'cucumber': VEGETABLE,
    'celery': VEGETABLE,
    'orange': FRUIT,
    'strawberry': FRUIT,
    'apple': FRUIT,
    'carrot': VEGETABLE
}

def load_companies():
    companies = []
    with open('%s/companies.json' % RESOURCE_DIR) as companies_file:
        companies = json.load(companies_file)
    return companies

def load_people():
    companies = []
    with open('%s/people.json' % RESOURCE_DIR) as people_file:
        people = json.load(people_file)
    return people

def companies_map():
    companies = load_companies()
    return {(c['index'] + 1):{'index': c['index'], 'name': c['company']} for c in companies}

def people_map():
    people = load_people()
    return {p['index']:p for p in people}

def people_food_vocabulary(people):
    food = list(map(lambda p: p['favouriteFood'], people))
    return set(itertools.chain.from_iterable(food))

def food_category(food):
    """ Returns the food category of a food item or unknown if no category is associated """
    return FOOD_CATEGORY.get(food, 'unknown')

def show_people_food_vocabulary():
    """ Shows all the possible food names we can find in dataset """
    vocabulary = people_food_vocabulary(load_people())
    for f in vocabulary: print('%s from %s' % (f, food_category(f)))

def prepare_embedded_friend(friend):
    """ Build person's friend embedded representation """
    return {
        'guid': friend['guid'],
        'index': friend['index'],
        'has_died': friend['has_died'],
        'eye_color': friend['eyeColor'],
        'name': friend['name'],
        'gender': friend['gender']
    }

def prepare_person_document(person, companies_map, people_map):
    """ From a person, create a document to be store in NoSQL database which will embed all person information
    We take advantage of this function to do some data manipulation:
    - normalize property keys
    - separate favourite food in 2 collections : vegatables and fruits
    - embed company information
    - embed friends information
    """
    embedded = copy.copy(person)
    embedded.pop('favouriteFood', None)
    embedded.pop('company_id', None)
    embedded.pop('eyeColor', None)
    embedded['eye_color'] = person['eyeColor']
    embedded['company'] = companies_map[person['company_id']]
    embedded['favourite_food'] = {
        'vegatables': list(filter(lambda f: food_category(f) == VEGETABLE, person['favouriteFood'])),
        'fruits': list(filter(lambda f: food_category(f) == FRUIT, person['favouriteFood']))
    }
    # Join person friends list with people map to store full friends description
    embedded['friends'] = list(map(lambda f: prepare_embedded_friend(people_map[f['index']]), person['friends']))
    return embedded

