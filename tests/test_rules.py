from exacto.scanner import Scanner
from exacto.rules import Rule


class TestRules:

    def test_base_rule(self):
        rule = Rule()
        scanner = Scanner()
        assert rule(scanner) is False
