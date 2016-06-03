class RedefinitionError(ValueError):
    """Raised when a substance is redefined.
    """

    def __init__(self, name, filename=None, lineno=None):
        super(ValueError, self).__init__()
        self.name = name
        self.filename = None
        self.lineno = None

    def __str__(self):
        msg = "cannot redefine '{0}'".format(self.name,
                                                   )
        if self.filename:
            mess = "While opening {0}, in line {1}: "
            return mess.format(self.filename, self.lineno) + msg
        return msg

class DefinitionSyntaxError(ValueError):
    """Raised when a textual definition has a syntax error.
    """

    def __init__(self, msg, filename=None, lineno=None):
        super(ValueError, self).__init__()
        self.msg = msg
        self.filename = None
        self.lineno = None

    def __str__(self):
        mess = "While opening {0}, in line {1}: "
        return mess.format(self.filename, self.lineno) + self.msg