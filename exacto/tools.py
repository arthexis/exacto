import io
from typing import Iterable, Callable

from .rules import *

__all__ = ["split", "lift"]


def split(text, *args: Callable, dense=True) -> Iterable[str]:
    """
    Split text according to list of rules applied in order.
    The "space" (split on whitespace) rule is used if no rules are specified.

    :param text: The text to split.
    :param args: A list of Rule instances or strings.
    :param dense: If true (default), exclude empty fragments.
    :return: A generator that yields string fragments.

    Frequently used recipes:

    >>> # Split on whitespace, returning a dense list
    >>> list(split("Hello   World "))
    ["Hello", "World"]

    >>> # Split on a delimiter, like str.split
    >>> tuple(split("Foo.Bar.Foo", delimit(".")))
    ("Foo", "Bar", "Foo)

    >>> # Split on whitespace except within quotes
    >>> from exacto.rules import quote
    >>> list(split("Hello 'What a Beautiful' World", quote))
    ["Hello", "'What a Beautiful'", "World"]
    """

    src = io.StringIO(text)
    return _apply(src, *args, dense=dense, op="split")


def lift(text, *args: Callable):
    """
    Lift tokens out of a text, discarding everything else.

    :param text: The text to lift.
    :param args: A list of Rule instances or strings.
    :return: A generator that yields string fragments.

    Frequently used recipes:

    >>> # Lift tokens out of a text
    >>> list(lift("Hello [FOO] World [BAR]", nest("[", "]")))
    ["FOO", "BAR"]
    """

    src = io.StringIO(text)
    return _apply(src, *args, clear, dense=True, op="lift", strip=True)


def _apply(src, *args: Callable, **kwargs) -> Iterable[str]:
    """Common implementation of split and lift tools."""

    dense = kwargs.get("dense", True)
    buffer = []
    rules = [
        delimit(r) if isinstance(r, str) else r
        for r in (args or (space, ))
    ]
    val = src.read(1)                       # Read 1 char at a time
    while val:
        buffer.append(val)                  # Keep chars read in buffer
        for rule in rules:
            if rule(buffer, **kwargs):      # Buffer is mutated by rule
                text = "".join(buffer)      # If True, split here
                if not dense or text:
                    yield text
                buffer.clear()              # Reset the buffer after split
            if not buffer:
                break                       # Skip rules if no buffer
        val = src.read(1)
    if buffer:
        text = "".join(buffer)              # Yield remainder in buffer
        if not dense or text:
            yield text
        buffer.clear()
    for rule in rules:
        rule(buffer, **kwargs)              # One last squeeze
        if buffer:
            text = "".join(buffer)          # Yield the last squeeze
            if not dense or text:
                yield text
            break
