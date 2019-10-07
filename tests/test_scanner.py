from exacto.scanner import Scanner


class TestScanner:

    def test_add_text_current(self):
        text = "Foo"
        scanner = Scanner()
        scanner.add_to_text(text)

        assert scanner.current == "F"
        assert scanner.peek(3) == "Foo"
