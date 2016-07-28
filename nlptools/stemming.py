import re

class Rule:
    def __init__(self, suffix, replacement):
        self.suffix = r"{}$".format(suffix)
        self.replacement = replacement

    def match_length(self, word):
        match = re.match(self.suffix)
        if match:
            return match.end() - match.start() + 1
        else:
            return 0

    def __call__(self, word):
        return re.sub(self.suffix, self.replacement, word)


def porter(word):
    rules = [Rule("ies", "i"), Rule("s", "")]

    for rule in rules:
        word = rule(word)

    return word