import unittest
from pathlib import Path
import os, sys, json
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
from src.compile_word_counts import get_word_counts
from src.compute_pony_lang import get_tfidf


class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
        

    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        with open(self.true_word_counts, 'r') as file:
            true_counts = json.load(file)
        # print(get_word_counts(self.mock_dialog, 1))
        
        self.assertEqual(true_counts, get_word_counts(self.mock_dialog, 1))

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        with open(self.true_tf_idfs, 'r') as file:
            true_tfidf = json.load(file)
        # print(get_tfidf(get_word_counts(self.mock_dialog, 1),3))
        
        self.assertEqual(true_tfidf, get_tfidf(get_word_counts(self.mock_dialog, 1),3))
        
    
if __name__ == '__main__':
    unittest.main()