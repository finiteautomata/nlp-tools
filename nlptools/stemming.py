import re
import operator

class Rule:
    def __init__(self, suffix, replacement, condition=None):
        self.suffix = r"{}$".format(suffix)
        self.replacement = replacement
        self.condition = condition or (lambda x: True)

    def match_length(self, word):
        match = re.search(self.suffix, word)

        if match:
            # Match should always be a suffix
            stem = word[:match.start()]
            if self.condition(stem):
                return match.end() - match.start()

        return 0

    def __call__(self, word):
        return re.sub(self.suffix, self.replacement, word)

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
            word = best_rule(word)

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
    rules = SetOfRules([
        Rule("sses", "ss"),
        Rule("ies", "i"),
        Rule("ss", "ss"),
        Rule("s", "")])

    stem = rules.apply(word)

    stem = SetOfRules([
        Rule("eed", "ee", lambda stem: measure(stem) > 0)
    ]).apply(stem)

    return stem