import inspect

from rules import *


class Ruleset:
    """An iterable of Rule instances."""

    def __init__(self, rules):
        self.rules = []
        for rule in rules:
            if inspect.isclass(rule):
                self.rules.append(rule())
            elif isinstance(rule, str):
                self.rules.append(Delimit(rule))
            else:
                self.rules.append(rule)

    def __iter__(self):
        return iter(self.rules)