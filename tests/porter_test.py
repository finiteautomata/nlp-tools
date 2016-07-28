import unittest
from nlptools.stemming import porter, Rule

class StemmingTest(unittest.TestCase):
    def test_comput_equals_to_comput(self):
        self.assertEqual(porter("comput"), "comput")

    def test_ponies_maps_to_poni(self):
        self.assertEqual(porter("ponies"), "poni")


class RuleTest(unittest.TestCase):
    def test_a_word_that_doesnt_finish_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule("foo"), "foo")

    def test_a_word_that_finishes_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule("flies"), "fli")

if __name__ == '__main__':
    unittest.main()