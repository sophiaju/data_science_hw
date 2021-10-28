import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.clean import clean
import json

class CleanTest(unittest.TestCase):
    def setUp(self):
        di = os.path.dirname(__file__)
        self.fixture = {}
        # load each fixture into dict
        for i in range(1,7):
            fixture_path = os.path.join(di, 'fixtures', f'test_{i}.json')
            with open(fixture_path) as file:
                self.fixture[i] = file.readline()

        
    # my clean function includes every constraint, so I call it each time
    def test_title(self):
        self.assertEqual(clean(self.fixture[1]), None)

    def test_date(self):
        self.assertEqual(clean(self.fixture[2]), None)

    def test_inv(self):
        self.assertEqual(clean(self.fixture[3]), None)
    
    def test_auth(self):
        self.assertEqual(clean(self.fixture[4]), None)
    
    def test_count(self):
        self.assertEqual(clean(self.fixture[5]), None)
    
    def test_tags(self):
        self.assertEqual(len(clean(self.fixture[6])["tags"]), 4)
        
        
if __name__ == '__main__':
    unittest.main()