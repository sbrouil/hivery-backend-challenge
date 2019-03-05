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

def get_by_guid(guid, projection=None):
    db = get_db()
    result = db.people.find_one({ 'guid': guid }, projection)
    if result is None:
        raise NotFound(guid)
    else:
        return result

def get_person_favourite_food(guid):
    db = get_db()
    return get_by_guid(guid, {'favourite_food': 1, 'name': 1, 'age': 1})