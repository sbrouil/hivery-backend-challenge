from flask import Blueprint, jsonify
from backend.validation import validate_uuid
import backend.store.people as people_store

people_v1 = Blueprint('people_v1', __name__)

@people_v1.route('/<guid>', methods=['GET'])
def get_person(guid):
    validate_uuid(guid)
    
    return jsonify(people_store.get_by_guid(guid))

@people_v1.route('/<guid>/favourite-food', methods=['GET'])
def get_person_favourite_food(guid):
    validate_uuid(guid)

    person = people_store.get_person_favourite_food(guid)
    favourite_food = person['favourite_food']

    return jsonify({
        'username': person['name'],
        'age': person['age'],
        'fruits': favourite_food['fruits'],
        'vegetables': favourite_food['vegetables']
    })
