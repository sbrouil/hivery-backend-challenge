from backend.db import get_db
from backend.exceptions import NotFound

def get_by_name(name):
    db = get_db()
    result = db.companies.find_one({ 'name': name },  {'_id': False})
    if result is None:
        raise NotFound('Company', name)
    else:
        return result