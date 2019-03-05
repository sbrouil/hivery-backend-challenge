from flask import current_app, g
from pymongo import MongoClient

def get_db():
    mongoConfig = current_app.config['mongodb']
    client = MongoClient(mongoConfig['host'], mongoConfig['port'])
    db = client[mongoConfig['database']]
    if 'db' not in g:
        g.db = db
    return g.db