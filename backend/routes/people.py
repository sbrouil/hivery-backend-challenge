import copy
from flask import Blueprint, jsonify, request
from backend.routes.validation import validate_uuid, bool_param_type
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

@people_v1.route('/<guid_source>/mutual-friends/<guid_target>', methods=['GET'])
def get_persons_mutual_friends(guid_source, guid_target):
    eye_color = request.args.get('eye_color', default = None, type = str)
    has_died = request.args.get('has_died', default = None, type = bool_param_type)

    source = people_store.get_by_guid_with_friends(guid_source, eye_color, has_died)
    target = people_store.get_by_guid_with_friends(guid_target, eye_color, has_died)

    # compute mutal friends
    sourceFriendDict = {f['guid']:f for f in source['friends']}
    targetFriendDict = {f['guid']:f for f in target['friends']}
    commonFriends = sourceFriendDict.keys() & targetFriendDict.keys()
    mutualFriends = [sourceFriendDict[guid] for guid in commonFriends]

    del source['friends']
    del target['friends']

    return jsonify({
        'source': source,
        'target': target,
        'mutual_friends': mutualFriends
    })