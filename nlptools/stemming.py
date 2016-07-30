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
        if len(word) > 1 and
            word[-1] == word[-2] and not
            word[-1] in ['l', 's', 'z']:
            return 2
        else:
            return 0

    def apply(self, word):
        return word[:-1]

class SetOfRules:
    def __init__(self, rules):
        self.rules = rules

    def find_best_rule(self, word):
        matches = map(lambda r: r.match_length(word), self.rules)

        best_match_index, match_length = max(enumerate(matches), key=operator.itemgetter(1))

        if match_length > 0:
            return self.rules[best_match_index]

    def apply(self, word):
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
    This is step 1a
    """
    rules = SetOfRules([
        Rule("sses", "ss"),
        Rule("ies", "i"),
        Rule("ss", "ss"),
        Rule("s", "")])

    stem = rules.apply(word)

    """
    step 1b

    callback_rules are the rules that are applied if second or third rules apply


    """
    callback_rules = SetOfRules([
        Rule('at', 'ate'),
        Rule('bl', 'ble'),
        Rule('iz', 'ize'),
        SingleLetterRule()
    ])

    has_vowel = lambda stem: 'V' in pattern(stem)[:-1]
    rules_1b = SetOfRules([
        Rule("eed", "ee", lambda stem: measure(stem) > 0),
        # This shit of [:-1] is not trustable at all
        Rule("ed", "", has_vowel, callback_rules),
        Rule("ing", "", has_vowel, callback_rules)
    ])

    stem = rules_1b.apply(stem)

    return stem