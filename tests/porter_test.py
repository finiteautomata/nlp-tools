import unittest
from nlptools.stemming import porter, Rule, measure, pattern

class StemmingTest(unittest.TestCase):
    def test_comput_equals_to_comput(self):
        self.assertEqual(porter("comput"), "comput")

    def test_ponies_maps_to_poni(self):
        self.assertEqual(porter("ponies"), "poni")

    def test_caresses_maps_to_caress(self):
        self.assertEqual(porter("caresses"), "caress")

class MeasureTest(unittest.TestCase):
    def test_measure_of_tree_equals_zero(self):
        self.assertEqual(measure("tree"), 0)


    def test_measure_of_tr_equals_zero(self):
        self.assertEqual(measure("tr"), 0)

    def test_measure_of_trouble_equals_one(self):
        self.assertEqual(measure("trouble"), 1)

    def test_measure_of_oats(self):
        self.assertEqual(measure("oats"), 1)

    def test_measure_of_private(self):
        self.assertEqual(measure("private"), 2)

    def test_measure_of_privates(self):
        self.assertEqual(measure("privates"), 3)


class PatternTest(unittest.TestCase):
    def test_pattern_of_tree(self):
        self.assertEqual(pattern("tree"), "CV")

    def test_pattern_of_trouble(self):
        self.assertEqual(pattern("trouble"), "CVCV")

    def test_pattern_of_erlang(self):
        self.assertEqual(pattern("erlang"), "VCVC")


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