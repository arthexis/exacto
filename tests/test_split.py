from scissors import *  # The code to test


def test_split_default():
    text = "Hello World"
    expected = ["Hello", "World"]
    result = split(text)
    assert result == expected


def test_split_default_extra_space():
    text = "Hello   World"
    expected = ["Hello", "World"]
    result = split(text)
    assert result == expected


def test_split_default_non_dense():
    text = "Hello   World"
    expected = ["Hello", "", "", "World"]
    result = split(text, dense=False)
    assert result == expected


def test_split_quoted_delimit():
    text = "Hello 'This Nice' World"
    expected = ["Hello", "'This Nice'", "World"]
    result = split(text, Quote("'"))
    assert result == expected


def test_split_quoted_delimit_unquote():
    text = "Hello 'This Nice' World"
    expected = ["Hello", "This Nice", "World"]
    result = split(text, Quote("'", keep=False))
    assert result == expected


def test_split_escape_delimit():
    text = "Hello$.World"
    expected = ["Hello.World"]
    result = split(text, Escape("$"), on=".")
    assert result == expected
