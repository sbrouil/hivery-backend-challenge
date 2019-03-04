import json
import os
import itertools

RESOURCE_DIR = os.path.dirname(os.path.realpath(__file__)) + '/resources'

FOOD_CATEGORY = {
    'beetroot': 'vegetable',
    'banana': 'fruit',
    'cucumber': 'vegetable',
    'celery': 'vegetable',
    'orange': 'fruit',
    'strawberry': 'fruit',
    'apple': 'fruit',
    'carrot': 'vegetable'
}

def load_companies():
    companies = []
    with open( RESOURCE_DIR + '/companies.json') as companies_file:
        companies = json.load(companies_file)
    return companies

def load_people():
    companies = []
    with open( RESOURCE_DIR + '/people.json') as people_file:
        people = json.load(people_file)
    return people

def people_food_vocabulary(people):
    food = list(map(lambda p: p['favouriteFood'], people))
    return set(itertools.chain.from_iterable(food))

def food_category(food):
    return FOOD_CATEGORY.get(food, 'unknown')

def show_people_food_vocabulary():
    vocabulary = people_food_vocabulary(load_people())
    for f in vocabulary: print(f + ' from ' + food_category(f))