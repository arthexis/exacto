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

    def __call__(self, scanner:  "Scanner"):
        if scanner.peek(1).isspace():
            scanner.split()
            scanner.forward(1)
            return True
        scanner.consume(1)


class AlphaNum(Rule):
    """Splits on any non-alphanumeric character."""

    def __call__(self, scanner:  "Scanner"):
        if not scanner.peek(1).isalnum():
            scanner.split()
            scanner.forward(1)
            return True
        scanner.consume(1)


class Quote(Rule):
    """Prevents splitting between quotes."""

    __slots__ = ("on", "stored", "keep")

    def __init__(self, on="\"", keep=True):
        self.on = on
        self.stored = None
        self.keep = keep

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
        if self.stored is not None:
            value = scanner.read(1)
            self.stored.append(value)
            return True


class Quotes(Rule):
    """Prevents splitting between multiple quote types."""

    __slots__ = ("on", "match", "stored", "keep")

    def __init__(self, *on, keep=True):
        self.on = on or ("'", '"')
        self.match = None
        self.stored = None
        self.keep = keep

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
        if self.stored is not None:
            value = scanner.read(1)
            self.stored.append(value)
            return True


class Nested(Rule):
    """Allow fragments with nested parenthesis."""

    __slots__ = ("start", "close", "depth", "stored")

    def __init__(self, start="(", close=")"):
        self.start = start
        self.close = close
        self.depth = 0
        self.stored = None

    def __call__(self, scanner: "Scanner"):
        match = scanner.match(self.start, self.close)
        if match == self.start:
            if self.depth == 0:
                self.stored = []
            self.depth += 1
            value = scanner.read(len(match))
            self.stored.append(value)
            return True
        if self.depth > 0:
            value = scanner.read(1)
            self.stored.append(value)
            if match == self.close:
                self.depth -= 1
                if self.depth == 0:
                    text = "".join(self.stored)
                    scanner.add_to_buffer(text)
                    self.stored = None
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
