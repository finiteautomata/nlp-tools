import re
import operator

class Rule:
    def __init__(self, suffix, replacement):
        self.suffix = r"{}$".format(suffix)
        self.replacement = replacement

    def match_length(self, word):
        match = re.search(self.suffix, word)
        if match:
            return match.end() - match.start()
        else:
            return 0

    def __call__(self, word):
        return re.sub(self.suffix, self.replacement, word)

class SetOfRules:
    def __init__(self, rules):
        self.rules = rules

    def apply(self, word):
        matches = list(map(lambda r: r.match_length(word), self.rules))

        best_match_index, match_length = max(enumerate(matches), key=operator.itemgetter(1))

        if match_length > 0:
            word = self.rules[best_match_index](word)

        return word


def porter(word):
    rules = SetOfRules([
        Rule("sses", "ss"),
        Rule("ies", "i"),
        Rule("ss", "ss"),
        Rule("s", "")])

    return rules.apply(word)