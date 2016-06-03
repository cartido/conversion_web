import os
from .util import *
from .definitions import *
from .errors import *

class SubstanceRegistry(object):
    """The matter registry stores the definition of matters"""

    def __init__(self, filename = ''):
        self._substances = {}

        if filename == '':
            self.load_definitions('substance_EN.txt')
        elif filename is not None:
            self.load_definitions(filename)

    def get_density(self, substance):
        if isinstance(substance, str):
            return self._substances[substance]

    def load_definitions(self, file):
        """Add matters defined in a definition text file.
        """
        # Permit both filenames and line-iterables
        if isinstance(file, str):
            try:
                with open(file, encoding='utf-8') as fp:
                        return self.load_definitions(fp)
            except (RedefinitionError, DefinitionSyntaxError) as e:
                if e.filename is None:
                    e.filename = file
                raise e
            except Exception as e:
                msg = getattr(e, 'message', '') or str(e)
                raise ValueError('While opening {0}\n{1}'.format(file, msg))

        ifile = SourceIterator(file)
        for no, line in ifile:
                try:
                    self.define(Definition.from_string(line))
                except (RedefinitionError, DefinitionSyntaxError) as ex:
                    if ex.lineno is None:
                        ex.lineno = no
                    raise ex
                except Exception as ex:
                    #logger.error("In line {0}, cannot add '{1}' {2}".format(no, line, ex))
                    raise ex

    def define(self, substance):
        """Add substance to registry"""

        def _adder(name, density):
            if name in self._substances:
                raise RedefinitionError(name)

            self._substances[name] = density

        _adder(substance.name, substance.density)

        for alias in substance.aliases:
            _adder(alias, substance.density)


