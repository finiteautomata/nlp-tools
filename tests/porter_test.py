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
    pass

"""

All the test cases are dynamically generated here

"""
cases = {
    'comput': 'comput',
    'ponies': 'poni',
    'caresses': 'caress',
    'feed': 'feed',
    'agreed': 'agre',
    'plastered': 'plaster',
    'bled': 'bled',
    'motoring': 'motor',
    'sing': 'sing',
    'conflated': 'conflat',
    'troubling': 'trouble',
    'sized': 'size',
    'hopping': 'hop',
    'falling': 'fall',
    'falling': 'fall',
    'filing': 'file',
    'happy': 'happi',
    'relational': 'relat',
    'conditional': 'condit',
    'rational': 'ration',
    'valency': 'valenc',
    'hesitance': 'hesit',
    'digitizer': 'digit',
    'conformabli': 'conform',
    'radically': 'radic',
    'differently': 'differ',
    'vilely': 'vile',
    'analogously': 'analog',
    'vietnamization': 'vietnam',
    'predication': 'predic',
    'operator': 'oper',
    'feudalism': 'feudal',
    'decisiveness': 'decis',
    'hopefulness': 'hope',
    'callousness': 'callous',
    'formality': 'formal',
    'sensitivity': 'sensit',
    'sensibility': 'sensibl',
    'triplicate': 'triplic',
    'formative': 'form',
    'formalize': 'formal',
    'electricity': 'electr',
    'electrical': 'electr',
    'hopeful': 'hope',
    'goodness': 'good',
    'revival': 'reviv',
    'allowance': 'allow',
    'inference': 'infer',
    'airliner': 'airlin',
    'gyroscopic': 'gyroscop',
    'adjustable': 'adjust',
    'defensible': 'defens',
    'irritant': 'irrit',
    'replacement': 'replac',
    'adjustment': 'adjust',
    'adoption': 'adopt',
    'homologou': 'homolog',
    'communism': 'commun',
    'activate': 'activ',
    'angularity': 'angular',
    'analogous': 'analog',
    'effective': 'effect',
    'mesmerize': 'mesmer',
    'probate': 'probat',
    'controll': 'control',
    'roll': 'roll'
}

def create_test_case(klass, word, stem):
    def test_case(self):
        self.assertEqual(porter(word), stem)

    test_name = "test_{}_to_{}".format(word, stem)

    setattr(klass, test_name, test_case)

for (word, stem) in cases.items():
    create_test_case(StemmingTest, word, stem)

if __name__ == '__main__':
    unittest.main()