from scanner import Scanner


class Rule:
    """Default base for all Rules."""

    def __call__(self, scanner: "Scanner") -> bool:
        return False  # Return True to stop processing further rules


class Delimit(Rule):
    """Splits on character, defaults to any whitespace."""

    __slots__ = ("on")

    def __init__(self, on=None):
        self.on = [on] if isinstance(on, str) else on or []

    def __call__(self, scanner:  "Scanner"):
        if not self.on and scanner.peek(1).isspace():
            scanner.split()
            scanner.forward(1)
            return True
        for on in self.on:
            match = scanner.match(on)
            if match:
                scanner.split()
                scanner.forward(len(match))
                return True
        scanner.consume(1)


class Quote(Rule):
    """Prevents splitting between quotes."""

    __slots__ = ("patterns", "match", "stored", "keep")

    def __init__(self, *patterns, keep=True):
        self.patterns = patterns or "\"'"
        self.match = None
        self.stored = []
        self.keep = keep

    def __call__(self, scanner: "Scanner"):
        for p in [self.match] if self.match else self.patterns:
            match = scanner.match(p)
            if match:
                scanner.forward(len(match))
                if self.match:
                    text = "".join(self.stored)
                    if self.keep:
                        text = f"{self.match}{text}{self.match}"
                    self.match = None
                    self.stored.clear()
                    scanner.add_to_buffer(text)
                    return True
                self.match = match
                return True
        if self.match:
            value = scanner.read(1)
            self.stored.append(value)
            return True


class Escape(Rule):
    """Escapes especial characters."""

    __slots__ = ("match", "patterns")

    def __init__(self, *patterns):
        self.match = None
        self.patterns = patterns or "\\"

    def __call__(self, scanner:  "Scanner"):
        if self.match:
            scanner.consume(1)
            self.match = None
            return False
        for p in self.patterns:
            match = scanner.match(p)
            if match:
                scanner.forward(len(match))
                self.match = match
                return True
