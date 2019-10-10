from typing import List, Callable, Any

__all__ = [
    "space",
    "alphanum",
    "delimit",
    "quote",
    "nest",
    "escape",
    "clear",
    "method",
    "apply",
]


def space(buffer: List[str], **kwargs):
    """Rule: Split when any whitespace is found."""

    return buffer.pop() if buffer and buffer[-1].isspace() else False


def alphanum(buffer: List[str], **kwargs):
    """Rule: Split when any non-alphanumeric character is found."""

    return buffer.pop() if buffer and not buffer[-1].isalnum() else False


def method(name, *args, **kwargs):
    """Rule: Split when method name returns True."""

    # noinspection PyShadowingNames,PyDefaultArgument
    def inner(buffer: List[str], kw=kwargs, **kwargs):
        nonlocal name, args
        if buffer and getattr(buffer.pop(), name)(*args, **kw):
            return buffer.pop()

    return inner


def delimit(sep):
    """Rule: Split when a delimiter character is found."""

    sep, size = list(sep), len(sep)

    def inner(buffer: List[str], **kwargs):
        nonlocal sep, size
        if len(buffer) >= size and buffer[-size:] == sep:
            return [buffer.pop() for _ in range(size)]

    return inner


def quote(*seps, strip=False):
    """Rule: Prevent splits between quote characters."""

    stored, inners, match = [], [], []
    for _sep in seps:
        _sep, _size = list(_sep), len(_sep)

        # noinspection PyDefaultArgument,PyShadowingNames
        def inner(buffer: List[str], sep=_sep, size=_size, strip=strip, **kwargs):
            nonlocal stored, match
            if match and match != sep:
                return
            if stored:
                if not buffer:
                    text = "".join(stored)
                    if strip:
                        text = text[_size:-_size].strip()
                    buffer.append(text)
                else:
                    stored.append(buffer.pop())
                    if len(stored) >= size and match == stored[-size:]:
                        text = "".join(stored)
                        if strip:
                            text = text[_size:-_size].strip()
                        buffer.append(text)
                        stored.clear()
                        match.clear()
                        return strip
            elif len(buffer) >= size and sep == buffer[-size:]:
                for _ in range(size):
                    stored.insert(0, buffer.pop())
                match = sep[:]
                return strip

        inners.append(inner)
    return inners if len(inners) > 1 else inners[0]


def nest(start, finish, strip=False):
    """Rule: Prevent splits between two sets of nestable characters."""

    stored, level = [], 0
    start, finish = list(start), list(finish)
    ss, fs = len(start), len(finish)

    # noinspection PyUnusedLocal,PyShadowingNames
    def inner(buffer: List[str], strip=strip, **kwargs):
        nonlocal stored, level
        if level > 0:
            stored.append(buffer.pop())
            if len(stored) >= fs and finish == stored[-fs:]:
                level = max(level - 1, 0)
                if level == 0:
                    text = "".join(stored)
                    if strip:
                        text = text[ss:-fs].strip()
                    buffer.append(text)
                    stored.clear()
                    return strip
            elif len(stored) >= ss and start == stored[-ss:]:
                level += 1
        elif len(buffer) >= ss and start == buffer[-ss:]:
            for _ in range(ss):
                stored.insert(0, buffer.pop())
            level += 1
            return strip

    return inner


def escape(code):
    """Rule: Prevent splits between two sets of nestable characters."""

    code, size = list(code), len(code)
    escaping, escaped = False, []

    def inner(buffer: List[str], **kwargs):
        nonlocal escaping, escaped
        if escaping:
            escaped.append(buffer.pop())
            escaping = False
        elif len(buffer) >= size and buffer[-size:] == code:
            for _ in range(size):
                buffer.pop()
            escaping = True
        elif escaped:
            buffer.append("".join(escaped) + buffer.pop())
            escaped.clear()

    return inner


def clear(buffer: List[str], **kwargs):
    """Rule: Discard all unused fragments."""

    buffer.clear()
