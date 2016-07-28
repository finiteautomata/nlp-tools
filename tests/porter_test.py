import unittest
from nlptools.stemming import porter, Rule

class StemmingTest(unittest.TestCase):
    def test_comput_equals_to_comput(self):
        self.assertEqual(porter("comput"), "comput")

    def test_ponies_maps_to_poni(self):
        self.assertEqual(porter("ponies"), "poni")

    def test_caresses_maps_to_caress(self):
        self.assertEqual(porter("caresses"), "caress")

class RuleTest(unittest.TestCase):
    def test_a_word_that_doesnt_finish_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule("foo"), "foo")

    def test_a_word_that_finishes_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule("flies"), "fli")

    def test_match_length_for_a_non_matching_word(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.match_length("foo"), 0)

    def test_match_length_for_a_non_matching_word(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.match_length("flies"), 3)


if __name__ == '__main__':
    unittest.main()