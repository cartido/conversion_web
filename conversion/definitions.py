"""
    definitions

    Functions and classes related to substance definition

"""

from .errors import *

class Definition(object):

    def __init__(self, name, density, aliases):
        self._name = name
        self._density = density
        self._aliases = aliases

    @classmethod
    def from_string(cls, definition):
        """Parse a definition"""

        if isinstance(definition, str):
            if '=' not in definition:
                raise DefinitionSyntaxError("Definition must contain '='")

            name, definition = definition.split('=', 1)
            name = name.strip()

            result = [res.strip() for res in definition.split('=')]
            density, aliases =  float(result[0]), tuple(result[1:])

            return SubstanceDefinition(name, density, aliases)
        else:
            raise DefinitionSyntaxError("Definition must be a string.")

    @property
    def name(self):
        return self._name

    @property
    def density(self):
        return self._density

    @property
    def aliases(self):
        return self._aliases

    def __str__(self):
        return self.name


class SubstanceDefinition(Definition):
    """Definition of a substance"""

    def __init__(self, name, density, aliases):
        super(SubstanceDefinition, self).__init__(name, density, aliases)