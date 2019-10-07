from .scanner import *
from .ruleset import *


def split(text, *args, on=Space, dense=True, strip=True) -> List[str]:
    """
    Split text according to list of rules applied in order.
    By default a Delimit() rule is automatically appended.

    :param text: The text to split.
    :param args: A list of Rule classes or instances.
    :param on: Use to override the final Delimit rule.
    :param dense: If True (the default), exclude empty elements.
    :param strip: f True (the default), run each fragment through strip.

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
            if strip:
                yield _scanner.pop_result(0).strip()
            else:
                yield _scanner.pop_result(0)

    if strip:
        yield _scanner.tail.strip()
    else:
        yield _scanner.tail


if __name__ == "__main__":
    pass
