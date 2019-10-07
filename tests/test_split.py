from scissors import *  # The code to test


class TestSplit:

    def test_default(self):
        text = "Hello World"
        actual = split(text)
        expected = ["Hello", "World"]
        assert actual == expected

    def test_whitespace_dense(self):
        text = "Hello   World"
        actual = split(text)
        expected = ["Hello", "World"]
        assert actual == expected

    def test_whitespace_no_dense(self):
        text = "Hello   World"
        actual = split(text, dense=False)
        expected = ["Hello", "", "", "World"]
        assert actual == expected

    def test_single_quoted(self):
        text = "Hello 'This Nice' World"
        actual = split(text, Quote("'"))
        expected = ["Hello", "'This Nice'", "World"]
        assert actual == expected

    def test_single_quoted_no_keep(self):
        text = "Hello 'This Nice' World"
        actual = split(text, Quote("'", keep=False))
        expected = ["Hello", "This Nice", "World"]
        assert actual == expected

    def test_long_delimiter(self):
        text = "Hello#@#World Test"
        actual = split(text, on="#@#")
        expected = ["Hello", "World Test"]
        assert actual == expected

    def test_escape_delimiter(self):
        text = "Hello$.World"
        actual = split(text, Escape("$"), on=".")
        expected = ["Hello.World"]
        assert actual == expected

    def test_strip(self):
        text = "Hello . World"
        actual = split(text, on=".")
        expected = ["Hello", "World"]
        assert actual == expected

    def test_no_strip(self):
        text = "Hello . World"
        actual = split(text, on=".", strip=False)
        expected = ["Hello ", " World"]
        assert actual == expected

    def test_nested_single(self):
        text = "Hello (good point) World"
        actual = split(text, Nested)
        expected = ["Hello", "(good point)", "World"]
        assert actual == expected

    def test_nested_double(self):
        text = "Hello (good (po int) yes) World"
        actual = split(text, Nested)
        expected = ["Hello", "(good (po int) yes)", "World"]
        assert actual == expected

    def test_alphanum(self):
        text = "Hello. This is a test."
        actual = split(text, on=AlphaNum)
        expected = ["Hello", "This", "is", "a", "test"]
        assert actual == expected

    def test_nested_quote_delimit(self):
        text = "ENV='Test Env'.PARAM=[SRC.PARAM].VAL"
        actual = split(text, Quote("'"), Nested("[", "]"), on=".")
        expected = ["ENV='Test Env'", "PARAM=[SRC.PARAM]", "VAL"]
        assert actual == expected

    def test_nested_double_quote_delimit(self):
        text = "ENV='Test Env'.PARAM=[SRC.PARAM].VAL=\"NEXT.ENV\""
        actual = split(text, Quote("'"), Quote('"'), Nested("[", "]"), on=".")
        expected = ["ENV='Test Env'", "PARAM=[SRC.PARAM]", "VAL=\"NEXT.ENV\""]
        assert actual == expected

    def test_multi_quote_space(self):
        text = "ENV='Test \"More Space\" Env' PARAM"
        actual = split(text, Quotes)
        expected = ["ENV='Test \"More Space\" Env'", "PARAM"]
        assert actual == expected

    def test_multi_quote_explicit_space(self):
        text = "ENV=$Test -More Space- Env$ PARAM"
        actual = split(text, Quotes("$", "-"))
        expected = ["ENV=$Test -More Space- Env$", "PARAM"]
        assert actual == expected

    def test_nested_quotes_backwards(self):
        text = "ENV='Test \"More Space\" Env' PARAM"
        actual = split(text, Quotes)
        expected = ["ENV='Test \"More Space\" Env'", "PARAM"]
        assert actual == expected

