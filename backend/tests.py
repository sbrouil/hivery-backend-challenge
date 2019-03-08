import unittest
from backend import create_app
from backend.db import get_db

class RestTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'mongodb': {
                'host': 'localhost',
                'port': 27017,
                'database': 'hivery_integration_test'
            }
        })
        self.client = self.app.test_client()    
        with self.app.app_context():
            self.db = get_db()
            # erase all existing data to ensure tests are independant
            self.db.people.drop()
            self.db.companies.drop()
     