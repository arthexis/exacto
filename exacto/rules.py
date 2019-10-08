import warnings

from .scanner import Scanner


class Rule:
    """Default base for all Rules."""

    def __call__(self, scanner: "Scanner") -> bool:
        return False  # Return True to stop processing further rules


class Delimit(Rule):
    """Splits on a specific delimiter string."""

    __slots__ = ("on")

    def __init__(self, on):
        self.on = on

    def __call__(self, scanner:  "Scanner"):
        match = scanner.match(self.on)
        if match:
            scanner.split()
            scanner.forward(len(match))
            return True
        scanner.consume(1)


class Space(Rule):
    """Splits on whitespace."""

    __slots__ = ()

    def __call__(self, scanner:  "Scanner"):
        if scanner.peek(1).isspace():
            scanner.split()
            scanner.forward(1)
            return True
        scanner.consume(1)


class AlphaNum(Rule):
    """Splits on any non-alphanumeric character."""

    __slots__ = ()

    def __call__(self, scanner:  "Scanner"):
        if not scanner.peek(1).isalnum():
            scanner.split()
            scanner.forward(1)
            return True
        scanner.consume(1)


class Quote(Rule):
    """Prevents splitting between quotes."""

    __slots__ = ("on", "stored", "keep", "stream", "warn")

    def __init__(self, on="\"", keep=True, stream=False, warn=True):
        self.on = on
        self.stored = None
        self.keep = keep
        self.stream = stream
        self.warn = warn

    def __call__(self, scanner: "Scanner"):
        match = scanner.match(self.on)
        if match:
            scanner.forward(len(match))
            if self.stored is None:
                self.stored = []
            else:
                text = "".join(self.stored)
                if self.keep:
                    text = f"{self.on}{text}{self.on}"
                self.stored = None
                scanner.add_to_buffer(text)
            return True
        return self._post_match(scanner, self.on)

    def _post_match(self, scanner: "Scanner", expected):
        if self.stored is not None:
            value = scanner.read(1)
            self.stored.append(value)
            if not self.stream and scanner.finished:
                scanner.add_to_buffer("".join(self.stored))
                self.stored = None
                if self.warn:
                    warnings.warn(f"Missing '{expected}' in text.")
            return True


class MultiQuote(Quote):
    """Prevents splitting between multiple quote types."""

    __slots__ = ("on", "match", "stored", "keep", "stream", "warn")

    def __init__(self, *on, keep=True, stream=False, warn=False):
        super().__init__(on or ("'", '"'), keep=keep, stream=stream, warn=warn)
        self.match = None

    def __call__(self, scanner: "Scanner"):
        match = scanner.match(*self.on)
        if match:
            scanner.forward(len(match))
            if self.stored is None:
                self.stored = []
                self.match = match
            elif match == self.match:
                text = "".join(self.stored)
                if self.keep:
                    text = f"{self.match}{text}{self.match}"
                self.stored = None
                self.match = None
                scanner.add_to_buffer(text)
            else:
                self.stored.append(match)
            return True
        return self._post_match(scanner, self.match)


class Nested(Rule):
    """Allow fragments with nested parenthesis."""

    __slots__ = ("start", "close", "depth", "stored", "stream", "warn")

    def __init__(self, start="(", close=")", stream=False, warn=True):
        self.start = start
        self.close = close
        self.depth = 0
        self.stored = None
        self.stream = stream
        self.warn = warn

    def pop_stored(self):
        text = "".join(self.stored)
        self.stored = None
        return text

    def __call__(self, scanner: "Scanner"):
        match = scanner.match(self.start, self.close)
        if match == self.start:
            if self.depth == 0:
                self.stored = []
            self.depth += 1
            self.stored.append(scanner.read(len(match)))
            return True
        if self.depth > 0:
            self.stored.append(scanner.read(1))
            if match == self.close:
                self.depth -= 1
                if self.depth == 0:
                    scanner.add_to_buffer(self.pop_stored())
            elif not self.stream and scanner.finished:
                scanner.add_to_buffer(self.pop_stored())
                self.depth = 0
                if self.warn:
                    warnings.warn(f"Missing '{self.close}' in text.")
            return True


class Escape(Rule):
    """Escapes especial characters."""

    __slots__ = ("on", "escaped")

    def __init__(self, on):
        self.escaped = False
        self.on = on

    def __call__(self, scanner:  "Scanner"):
        if self.escaped:
            scanner.consume(1)
            self.escaped = False
            return False
        match = scanner.match(self.on)
        if match:
            scanner.forward(len(match))
            self.escaped = True
            return True
