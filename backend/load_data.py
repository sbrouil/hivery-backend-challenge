import data
import json
import config
from pymongo import MongoClient

def import_data():
    """ Import data to the database from JSON dataset file after erasing previous content
    The whole operation is performed in memory cause the dataset is small (no more than 1000 items)
    The mongo insertion method does not use batch insert for similar reason.
    This is a one shot operation done during application installation step.
    """
    print('Load data:')
    people = data.load_people()
    companies_map = data.companies_map()
    people_map = data.people_map()

    mongoConfig = config.get('mongodb')
    client = MongoClient(mongoConfig['host'], mongoConfig['port'])
    db = client[mongoConfig['database']]
    people_collection = db.people
    people_collection.drop()

    inserted_count = 0
    for p in people:
        doc = data.prepare_person_document(p, companies_map, people_map)
        print('Inserting %s' % p['name'])
        people_collection.insert_one(doc)
        inserted_count += 1
    print('%d people documents inserted' % inserted_count)

import_data()