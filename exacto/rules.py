from typing import List, Callable, Any

__all__ = [
    "space",
    "alphanum",
    "delimit",
    "quote",
    "nest",
    "escape",
]


def space(buffer: List[str]):
    return buffer.pop() if buffer and buffer[-1].isspace() else False


def alphanum(buffer: List[str]):
    return buffer.pop() if buffer and not buffer[-1].isalnum() else False


def delimit(sep):
    sep, size = list(sep), len(sep)

    def inner(buffer: List[str]):
        if len(buffer) >= size and buffer[-size:] == sep:
            return [buffer.pop() for _ in range(size)]

    return inner


def quote(*seps):
    stored, inners, match = [], [], []

    for _sep in seps:
        _sep, _size = list(_sep), len(_sep)

        # noinspection PyDefaultArgument
        def inner(buffer: List[str], sep=_sep, size=_size):
            nonlocal stored, match
            if match and match != sep:
                return
            if stored:
                if not buffer:
                    buffer.append("".join(stored))
                else:
                    stored.append(buffer.pop())
                    if len(stored) >= size and match == stored[-size:]:
                        buffer.append("".join(stored))
                        stored.clear()
                        match.clear()
            elif len(buffer) >= size and sep == buffer[-size:]:
                for _ in range(size):
                    stored.insert(0, buffer.pop())
                match = sep[:]

        inners.append(inner)
    return inners if len(inners) > 1 else inners[0]


def nest(start, finish):
    stored, level = [], 0

    def inner(buffer: List[str]):
        nonlocal stored, level
        if level > 0:
            stored.append(buffer.pop())
            if finish == stored[-1]:
                level = max(level - 1, 0)
                if level == 0:
                    buffer.append("".join(stored))
                    stored.clear()
            elif start == stored[-1]:
                level += 1
        elif start == buffer[-1]:
            stored.append(buffer.pop())
            level += 1

    return inner


def escape(code):
    code, size = list(code), len(code)
    escaping, escaped = False, []

    def inner(buffer: List[str]):
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

