from exacto.rules import *


class TestRule:

    def test_space_done(self):
        buffer = list("Foo ")
        done = space(buffer)
        assert buffer == list("Foo")
        assert done

    def test_delimit_done(self):

        buffer = list("Foo+")
        done = delimit("+")(buffer)
        assert buffer == list("Foo")
        assert done

    def test_quote(self):
        func = quote("'")
        original = list("Hello 'World'")
        buffer = []
        for char in original:
            buffer.append(char)
            done = func(buffer)
        assert buffer == list("Hello ") + ["'World'"]

    def test_multi_quote(self):
        funcs = quote("'", '"')
        assert len(funcs) == 2
