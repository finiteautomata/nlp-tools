import re
import operator

class EmptyRule:
    def apply(self, word):
        return word

class Rule:
    def __init__(self, suffix, replacement, condition=None, callback_rule=None):
        self.suffix = r"{}$".format(suffix)
        self.replacement = replacement
        self.condition = condition or (lambda x: True)
        self.callback_rule = callback_rule or EmptyRule()

    def match_length(self, word):
        match = re.search(self.suffix, word)

        if match:
            # Match should always be a suffix
            stem = word[:match.start()]
            if self.condition(stem):
                return match.end() - match.start()

        return 0

    def apply(self, word):
        stem = re.sub(self.suffix, self.replacement, word)

        stem = self.callback_rule.apply(stem)

        return stem

class SingleLetterRule:
    def __init__(self):
        pass

    def match_length(self, word):
        if len(word) > 1:
            if word[-1] == word[-2] and not (word[-1] in ['l', 's', 'z']):
                return 2
        return 0

    def apply(self, word):
        return word[:-1]

class AddERule:
    def match_length(self, word):
        if pattern(word) == "CVC" and word[-1] not in ['w', 'x', 'y']:
            return 1
        return 0

    def apply(self, word):
        return word + 'e'

class SetOfRules:
    """
    This is a composite rule, in the sense of a GOF's Composite Pattern

    When applying this composite rule, it will apply the rule (if exists) with
    the longest matching subsequence.
    """
    def __init__(self, rules):
        self.rules = rules

    def find_best_rule(self, word):
        matches = map(lambda r: r.match_length(word), self.rules)

        best_match_index, match_length = max(enumerate(matches), key=operator.itemgetter(1))

        if match_length > 0:
            return self.rules[best_match_index]

    def apply(self, word):
        """
        Applies the rule with the longest matching subsequence.
        """
        best_rule = self.find_best_rule(word)

        if best_rule:
            word = best_rule.apply(word)

        return word

def pattern(word):
    """
    Returns an alternating sequence of V and C according to Porter's paper

    tree => "CV"
    trouble => "CVCV"
    """
    pattern = ""

    def get_type(word, pos):
        if word[pos] in ['a', 'e', 'i', 'o', 'u']:
            return 'V'
        else:
            return 'C'

    pattern = current_type = get_type(word, 0)

    for i in range(1, len(word)):
        new_type = get_type(word, i)
        if new_type != current_type:
            pattern += new_type
        current_type = new_type

    return pattern


def measure(word):
    """
    Returns the Porter's measure of a word.

    If word has a pattern C?(VC){n}V? then measure(word) returns n
    """

    if len(word) == 0:
        return 0

    form = pattern(word)

    if form[0] == "C" and form[-1] == "V":
        return len(form) // 2 - 1
    else:
        return len(form) // 2


def porter(word):

    """
    step 1b

    callback_rules are the rules that are applied if second or third rules apply
    """
    has_vowel = lambda stem: 'V' in pattern(stem)[:-1]
    measure_greater_one = lambda stem: measure(stem) > 1
    non_zero_measure = lambda stem: measure(stem) > 0

    callback_rules = SetOfRules([
        Rule('at', 'ate'),
        Rule('bl', 'ble'),
        Rule('iz', 'ize'),
        SingleLetterRule(),
        AddERule()
    ])

    steps = [
        # Step 1a
        SetOfRules([
            Rule("sses", "ss"),
            Rule("ies", "i"),
            Rule("ss", "ss"),
            Rule("s", "")]),
        # Step 1b
        SetOfRules([
            Rule("eed", "ee", non_zero_measure),
            # This shit of [:-1] is not trustable at all
            Rule("ed", "", has_vowel, callback_rules),
            Rule("ing", "", has_vowel, callback_rules)
        ]),
        # Step 1c
        SetOfRules([Rule("y", "i", has_vowel)]),
        # Step 2
        SetOfRules([
            Rule("ational", "ate", non_zero_measure),
            Rule("tional", "tion", non_zero_measure),
            Rule("enci", "ence", non_zero_measure),
            Rule("anci", "ance", non_zero_measure),
            Rule("izer", "ize", non_zero_measure),
            Rule("abli", "able", non_zero_measure),
            Rule("alli", "al", non_zero_measure),
            Rule("entli", "ent", non_zero_measure),
            Rule("eli", "e", non_zero_measure),
            Rule("ousli", "ous", non_zero_measure),
            Rule("ization", "ize", non_zero_measure),
            Rule("ation", "ate", non_zero_measure),
            Rule("ator", "ate", non_zero_measure),
            Rule("alism", "al", non_zero_measure),
            Rule("iveness", "ive", non_zero_measure),
            Rule("fulness", "ful", non_zero_measure),
            Rule("ousness", "ous", non_zero_measure),
            Rule("aliti", "al", non_zero_measure),
            Rule("iviti", "ive", non_zero_measure),
            Rule("biliti", "ble", non_zero_measure),
        ]),
        # Step 3
        SetOfRules([
            Rule("icate", "ic", non_zero_measure),
            Rule("ative", "", non_zero_measure),
            Rule("alize", "al", non_zero_measure),
            Rule("iciti", "ic", non_zero_measure),
            Rule("ical", "ic", non_zero_measure),
            Rule("ful", "", non_zero_measure),
            Rule("ness", "", non_zero_measure),
        ]),
        # Step 4
        SetOfRules([
            Rule("al", "", measure_greater_one),
            Rule("ance", "", measure_greater_one),
            Rule("ence", "", measure_greater_one),
            Rule("er", "", measure_greater_one),
            Rule("ic", "", measure_greater_one),
            Rule("able", "", measure_greater_one),
            Rule("ant", "", measure_greater_one),
            Rule("ement", "", measure_greater_one),
            Rule("ment", "", measure_greater_one),
            Rule("ent", "", measure_greater_one),
            Rule("ible", "", measure_greater_one),
            Rule("ion", "", lambda stem: stem[-1] in ['s', 't'] and measure_greater_one(stem)),
            Rule("ou", "", measure_greater_one),
            Rule("ism", "", measure_greater_one),
            Rule("ate", "", measure_greater_one),
            Rule("iti", "", measure_greater_one),
            Rule("ous", "", measure_greater_one),
            Rule("ive", "", measure_greater_one),
            Rule("ous", "", measure_greater_one),
            Rule("ize", "", measure_greater_one),
        ]),
    ]

    stem = word

    for step in steps:
        stem = step.apply(stem)

    return stem