from exacto.tools import *
from exacto.rules import *


class TestSplit:

    def test_default_space(self):
        text = "Hello World"
        actual = list(split(text))
        expected = ["Hello", "World"]
        assert actual == expected

    def test_space(self):
        text = "Hello World"
        actual = list(split(text, space))
        expected = ["Hello", "World"]
        assert actual == expected

    def test_delimit(self):
        text = "Hello.World"
        actual = list(split(text, delimit(".")))
        expected = ["Hello", "World"]
        assert actual == expected

    def test_delimit_multichar(self):
        text = "Hello#@#World"
        actual = list(split(text, delimit("#@#")))
        expected = ["Hello", "World"]
        assert actual == expected

    def test_delimit_dense(self):
        text = "Hello..World"
        actual = list(split(text, delimit(".")))
        expected = ["Hello", "World"]
        assert actual == expected

    def test_delimit_not_dense(self):
        text = "Hello..World"
        actual = list(split(text, delimit("."), dense=False))
        expected = ["Hello", "", "World"]
        assert actual == expected

    def test_quote(self):
        text = "Hello 'World' Again"
        actual = list(split(text, quote("'")))
        assert "".join(actual) == text

    def test_quote_leftover(self):
        text = "Hello 'World Again"
        actual = list(split(text, quote("'")))
        assert "".join(actual) == text

    def test_quote_space(self):
        text = "Hello 'This Example' Again"
        actual = list(split(text, quote("'"), space))
        expected = ["Hello", "'This Example'", "Again"]
        assert actual == expected

    def test_multi_quote_space(self):
        text = "Hello 'This Example' \"Another Example\" Again"
        actual = list(split(text, *quote("'", '"'), space))
        expected = ["Hello", "'This Example'", '"Another Example"', "Again"]
        assert actual == expected

    def test_nest_lv1_space(self):
        text = "Hello (This Example) World"
        actual = list(split(text, nest("(", ")"), space))
        expected = ["Hello", "(This Example)", "World"]
        assert actual == expected

    def test_nest_lv2_space(self):
        text = "Hello (This is (Another Interesting) Example) World"
        actual = list(split(text, nest("(", ")"), space))
        expected = ["Hello", "(This is (Another Interesting) Example)", "World"]
        assert actual == expected

    def test_nest_lv1_quote_space(self):
        text = "Hello (This 'One' Example) World"
        actual = list(split(text, nest("(", ")"), quote("'"), space))
        expected = ["Hello", "(This 'One' Example)", "World"]
        assert actual == expected

    def test_escape_delimit(self):
        text = "Hello$.World"
        actual = list(split(text, escape("$"), delimit(".")))
        expected = ["Hello.World"]
        assert actual == expected

    def test_escape_quote_delimit(self):
        text = "Hello-'Foo-$'-Bar'-World"
        actual = list(split(text, escape("$"), quote("'"), delimit("-")))
        expected = ["Hello", "'Foo-'-Bar'", "World"]
        assert actual == expected

    def test_alphanum(self):
        text = "Hello-Foo World.Tree"
        actual = list(split(text, alphanum))
        expected = ["Hello", "Foo", "World", "Tree"]
        assert actual == expected

