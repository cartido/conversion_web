

class SourceIterator(object):
    """Iterator to facilitate reading the definition files.

    Accepts any sequence (like a list of lines, a file or another SourceIterator)

    The iterator yields the line number and line (skipping comments and empty lines)
    and stripping white spaces.

    for lineno, line in SourceIterator(sequence):
        # do something here

    """

    def __new__(cls, sequence):
        if isinstance(sequence, SourceIterator):
            return sequence

        obj = object.__new__(cls)

        if sequence is not None:
            obj.internal = enumerate(sequence, 1)
            obj.last = (None, None)

        return obj

    def __iter__(self):
        return self

    def __next__(self):
        line = ''
        while not line or line.startswith('#'):
            lineno, line = next(self.internal)
            line = line.split('#', 1)[0].strip()

        self.last = lineno, line
        return lineno, line

    next = __next__

    def block_iter(self):
        """Iterate block including header.
        """
        return BlockIterator(self)