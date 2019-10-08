from .scanner import *
from .ruleset import *


def split(text, *args, on=Space, dense=True, strip=True) -> List[str]:
    """
    Split text according to list of rules applied in order.

    By default a Space rule is automatically appended at the end, if you use
    on to override this, you must use Delimit, Space, AlphaNum or a custom
    Rule that calls Scanner.split at some point.

    :param text: The text to split.
    :param args: A list of Rule classes or instances.
    :param on: The last rule to apply, defaults to Space.
    :param dense: If True (default), exclude empty elements.
    :param strip: If True (default), call str.strip on each fragment.

    Frequently used recipes:

    >>> # Split on whitespace, returning a dense list
    >>> split("Hello   World ")
    ["Hello", "World"]

    >>> # Split on whitespace except within quotes
    >>> split("Hello 'What a Beautiful' World")
    ["Hello", "'What a Beautiful'", "World"]
    """

    _scanner = Scanner(text, dense=dense)
    _ruleset = Ruleset((*args, on))

    while not _scanner.finished:
        for rule_function in _ruleset:
            if rule_function(_scanner):
                break

    if strip:
        return [f.strip() for f in _scanner.as_list()]
    return _scanner.as_list()


def iter_split(text, *args, on=Space, dense=True, strip=True) -> List[str]:
    """Same as split but return an iterator instead."""

    _scanner = Scanner(text, dense=dense)
    _ruleset = Ruleset((*args, on))

    while not _scanner.finished:
        for rule_function in _ruleset:
            if rule_function(_scanner):
                break
        if _scanner.ready:
            result = _scanner.pop_result(0)
            yield result.strip() if strip else result
    yield _scanner.tail.strip() if strip else _scanner.tail


if __name__ == "__main__":
    pass
