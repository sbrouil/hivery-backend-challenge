import unittest
from backend import create_app

class ConfigTest(unittest.TestCase):
    """ Config loading
    """
    def setUp(self):
        self.app = create_app()
        
    def test_config_loaded(self):
        self.assertIsNotNone(self.app.config['mongodb']['host'])