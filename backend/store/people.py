"""
# use case 1
db.getCollection('people').find({ 'company.index': 57})

# use case 2
db.getCollection('people').aggregate([
    {$match: { guid: '5e71dc5d-61c0-4f3b-8b92-d77310c7fa43'}},
    {
        $project: {
            name: 1,
            age: 1,
            address: 1,
            phone: 1,
            friends: {
                $filter: {
                    input: "$friends",
                    cond: { $and: [
                        { $eq: ["$$this.eye_color", "brown"]},
                        { $eq: ["$$this.has_died", false ]}
                    ] }
                }
            }
        }
    }
])

# use case 3
db.getCollection('people').findOne({ 'guid': '5e71dc5d-61c0-4f3b-8b92-d77310c7fa43'}, {'favourite_food': 1, 'name': 1, 'age': 1})
"""
from backend.db import get_db
from backend.exceptions import NotFound

# Hide some nested fields by default
DEFAULT_PERSON_PROJECTION = {
    '_id': False,
    'friends': False,
    'favourite_food': False,
    'tags': False
}

def get_by_guid(guid, projection={'_id': False}):
    db = get_db()
    result = db.people.find_one({ 'guid': guid }, projection)
    if result is None:
        raise NotFound('Person', guid)
    else:
        return result

def get_by_guid_with_friends(guid, friend_eye_color = None, friend_has_died = None):
    cond = []
    if friend_eye_color is not None:
        cond.append({ '$eq': ["$$this.eye_color", friend_eye_color]})
    if friend_has_died is not None:
        cond.append({ '$eq': ["$$this.has_died", friend_has_died ]})

    db = get_db()
    people = list(db.people.aggregate([
        {'$match': { 'guid': guid}},
        {
            '$project': {
                '_id': False,
                'name': True,
                'age': True,
                'address': True,
                'phone': True,
                'friends': {
                    '$filter': {
                        'input': '$friends',
                        'cond': { '$and': cond }
                    }
                }
            }
        }
    ]))
    if len(people) == 0:
        raise NotFound('Person', guid)
    return people[0]

def get_person_favourite_food(guid):
    db = get_db()
    return get_by_guid(guid, {'_id': False, 'favourite_food': True, 'name': True, 'age': True})

def get_people_by_company_name(name):
    db = get_db()
    # We are pulling the whole result into memory cause we generally have a reasonable number of employees
    # per company. If the volume becomes to large, plan to handle pagination in the service
    return list(db.people.find({ 'company.name': name }, DEFAULT_PERSON_PROJECTION))