from pymongo import MongoClient
from flask import current_app, g
from flask.cli import with_appcontext
from backend.resources import data_utils
import click

def get_db():
    mongoConfig = current_app.config['mongodb']
    client = MongoClient(mongoConfig['host'], mongoConfig['port'])
    db = client[mongoConfig['database']]
    if 'db' not in g:
        g.db = db
        g.client = client
    return g.db

def close_db():
    client = g.pop('client', None)
    if client is not None:
        client.close()

@click.command('load_data')
@with_appcontext
def load_data_command():
    """ Import data to the database from JSON dataset file after erasing previous content
    The whole operation is performed in memory cause the dataset is small (no more than 1000 items)
    The mongo insertion method does not use batch insert for similar reason.
    This is a one shot operation done during application installation step.
    """
    print('Load data:')
    people = data_utils.load_people()
    companies = data_utils.load_companies()
    companies_map = data_utils.companies_map()
    people_map = data_utils.people_map()

    db = get_db()
    db.companies.drop()
    db.people.drop()

    # inserting companies
    inserted_count = 0
    for c in companies:
        doc = {
            'index': c['index'],
            'name': c['company']
        }
        print('Inserting company %s' % c['company'])
        db.companies.insert_one(doc)
    print('%d companies inserted' % inserted_count)

    # inserting people
    inserted_count = 0
    for p in people:
        doc = data_utils.prepare_person_document(p, companies_map, people_map)
        print('Inserting person %s' % p['name'])
        db.people.insert_one(doc)
        inserted_count += 1
    print('%d people documents inserted' % inserted_count)

def init_app(app):
    """ Register flask command to load new data from .json files. 
        Will be called in the module in create_app() factory
    """
    app.cli.add_command(load_data_command)