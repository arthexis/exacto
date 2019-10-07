from typing import List, Optional


class Scanner:
    """Used by the split functions to scan the string."""

    __slots__ = ('text', 'len', 'pos', '_buffer', '_parts', '_tags', 'dense')

    def __init__(self, text=None, dense=True):
        self.text = text or ""  # The fragment being scanned
        self.pos = 0            # Current position in the fragment
        self._buffer = []
        self._parts = []
        self._tags = []
        self.dense = dense

    @property
    def finished(self):
        """True if we have scanned the whole fragment, False otherwise."""
        return self.pos >= len(self.text)

    @property
    def ready(self):
        """True if at least one result has been obtained."""
        return len(self._parts) and any(self._parts)

    def consume(self, n=1) -> None:
        """
        Add n characters from fragment to buffer and advance pos by n.
        :param n: Characters to consume.
        """

        fragment = self.text[self.pos: self.pos + (n or 0)]
        self._buffer.append(fragment)
        self.pos += len(fragment)

    def add_to_text(self, fragment) -> None:
        """Add another fragment at the end of the scanned text."""
        self.text += fragment

    def peek(self, n=1) -> str:
        """Look at the next n chars, don't advance scanner position."""
        return self.text[self.pos: self.pos + (n or 0)]

    @property
    def current(self):
        """Character at current position. Same as peek 1."""
        return self.text[self.pos]

    def match(self, *args) -> Optional[str]:
        """
        Check if any of args match the text at current position.
        :param args: A list of _parts to match against.
        :return: The matched string if found, else None.
        """
        for arg in args:
            if self.peek(len(arg)) == arg:
                return arg

    def forward(self, n=1) -> None:
        """Move the position forwards by n."""
        self.pos += (n or None)

    def read(self, n=1) -> str:
        """Read n characters at current position, then forward n."""
        r = self.text[self.pos: self.pos + n]
        self.pos += n
        return r

    def add_to_buffer(self, fragment) -> None:
        """
        Add arbitrary fragment to buffer.
        :param fragment: The text fragment added to buffer.
        """

        self._buffer.append(fragment)

    @property
    def tail(self):
        """Text not split, but currently in the buffer."""
        return "".join(self._buffer)

    def split(self, tag=None) -> None:
        """Split the current buffer."""

        if not self.dense or any(self._buffer):
            self._parts.append(self.tail)
            self._tags.append(tag)
            self._buffer.clear()

    def as_list(self):
        """Return the current results as a list."""
        if not self.dense or any(self._buffer):
            return [*self._parts, self.tail]
        return self._parts

    def pop_result(self, i=0):
        """Return and remove one of the stored result parts."""
        return self._parts.pop(i)
