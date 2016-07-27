import unittest
from nlptools import levenshtein

class LevenshteinTest(unittest.TestCase):
    def test_equals_to_zero_for_same_word(self):
        self.assertEqual(levenshtein("foo", "foo"), 0)

    def test_returns_len_of_string_to_empty_one(self):
        self.assertEqual(levenshtein("", "foo"), 3)

    def test_returns_len_of_string_to_empty_one(self):
        self.assertEqual(levenshtein("foo", ""), 3)

    def test_returns_1_for_last_different_character(self):
         self.assertEqual(levenshtein("kadafi", "kadafy"), 1)

    def test_returns_correct_result_for_many_operations(self):
         self.assertEqual(levenshtein("kadaffi", "gaddafy"), 4)

if __name__ == '__main__':
    unittest.main()