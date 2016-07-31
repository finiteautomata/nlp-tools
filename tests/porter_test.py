from unittest import TestCase
from unittest.mock import MagicMock
from nlptools.stemming import porter, Rule, measure, pattern


class MeasureTest(TestCase):
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


class PatternTest(TestCase):
    def test_pattern_of_tree(self):
        self.assertEqual(pattern("tree"), "CV")

    def test_pattern_of_trouble(self):
        self.assertEqual(pattern("trouble"), "CVCV")

    def test_pattern_of_erlang(self):
        self.assertEqual(pattern("erlang"), "VCVC")


class RuleTest(TestCase):
    def test_a_word_that_doesnt_finish_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.apply("foo"), "foo")

    def test_a_word_that_finishes_with_ies(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.apply("flies"), "fli")

    def test_match_length_for_a_non_matching_word(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.match_length("foo"), 0)

    def test_match_length_for_a_non_matching_word(self):
        rule = Rule("ies", "i")

        self.assertEqual(rule.match_length("flies"), 3)

    def test_a_rule_with_condition_not_met(self):
        rule = Rule("eed", "ee", lambda stem: False)

        self.assertEqual(rule.match_length("feed"), 0)


    def test_a_rule_with_condition_met(self):
        rule = Rule("eed", "ee", lambda stem: True)

        self.assertEqual(rule.match_length("agreed"), 3)

    def test_callback_is_called_when_condition_met(self):
        callback = MagicMock()
        callback.apply.return_value = "agree"

        rule = Rule("eed", "ee", lambda stem: True, callback)

        rule.apply("agreed")

        # Callback should be called with the resulting stem
        callback.apply.assert_called_with("agree")

class StemmingTest(TestCase):
    def test_comput_equals_to_comput(self):
        self.assertEqual(porter("comput"), "comput")

    def test_ponies_maps_to_poni(self):
        self.assertEqual(porter("ponies"), "poni")

    def test_caresses_maps_to_caress(self):
        self.assertEqual(porter("caresses"), "caress")

    def test_feed_to_feed(self):
        self.assertEqual(porter("feed"), "feed")

    def test_agreed_to_agree(self):
        self.assertEqual(porter("agreed"), "agree")

    def test_plastered_to_plaster(self):
        self.assertEqual(porter("plastered"), "plaster")

    def test_bled_to_bled(self):
        self.assertEqual(porter("bled"), "bled")

    def test_motoring_to_motor(self):
        self.assertEqual(porter("motoring"), "motor")

    def test_sing_to_sing(self):
        self.assertEqual(porter("sing"), "sing")

    def test_conflated_to_conflate(self):
        self.assertEqual(porter("conflated"), "conflate")

    def test_troubling_to_trouble(self):
        self.assertEqual(porter("troubling"), "trouble")

    def test_sized_to_size(self):
        self.assertEqual(porter("sized"), "size")

    def test_hopping_to_hop(self):
        self.assertEqual(porter("hopping"), "hop")

    def test_falling_to_fall(self):
        self.assertEqual(porter("falling"), "fall")

    def test_falling_to_fall(self):
        self.assertEqual(porter("falling"), "fall")

    def test_filing_to_file(self):
        self.assertEqual(porter("filing"), "file")

if __name__ == '__main__':
    unittest.main()