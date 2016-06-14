import re
import inflect
#from db import DbCaller
#from containers import Matter
from decimal import Decimal
from pint import UnitRegistry,DimensionalityError, UndefinedUnitError
from enum import Enum
from conversion.substance import *

class ConversionType(Enum):
    SameUnits = 1
    UsingDensity = 2

module_dir = os.path.dirname(__file__)  # get current directory

file_path = os.path.join(module_dir, 'definition_files/units_en.txt')
ureg = UnitRegistry(file_path)
sreg = SubstanceRegistry()


class PintParser:
    """ Parse and normalize a question
    """

    def __init__(self, raw_question):
        """
        :param source_measure:
        :param target_measure:
        :param substance:
        :param raw_question:
        :return:
        """
        try:
           # self.DbCaller = DbCaller()
            self.inflect = inflect.engine()

            self.raw_string = raw_question
            self.raw_source_unit = None
            self.source_unit = None
            self.source_dimension = None
            self.raw_target_unit = None
            self.target_unit = None
            self.target_dimension = None
            self.raw_substance = None
            self.substance = SubstanceDefinition
            self.response = None
            self.conversion_type = None
            self.error= None

            if raw_question :
                self.parse_raw_question()

            self.source_unit = self.normalize_measure(self.raw_source_unit, self.source_dimension)
            self.target_unit = self.normalize_measure(self.raw_target_unit, self.target_dimension)
            self.source_dimension = self.normalize_dimension(self.source_unit.dimensionality)
            self.target_dimension = self.normalize_dimension(self.target_unit.dimensionality)
            self.substance = self.define_substance(self.raw_substance)

            self.response = self.compute_response()
        except (DimensionalityError, UndefinedUnitError, UnedfinedSubstanceError, QuestionSyntaxError):
            pass
        except:
            raise
    def parse_raw_question(self):
        error = None
        parts_with_matter = re.match(r"(\d.*) of (.*) to (.*)$", self.raw_string)
        parts_without_matter = re.match(r"(\d.*) to (.*)$", self.raw_string)

        if parts_with_matter:
            self.raw_source_unit = parts_with_matter.group(1)
            self.raw_substance = parts_with_matter.group(2)
            self.raw_target_unit = parts_with_matter.group(3)
            self.conversion_type = ConversionType.UsingDensity
        elif parts_without_matter:
            self.raw_source_unit = parts_without_matter.group(1)
            self.raw_target_unit = parts_without_matter.group(2)
            self.conversion_type = ConversionType.SameUnits
        else:
            self.error = "'{question}' is not a valide conversion".format(question = self.raw_string)
            raise QuestionSyntaxError("'{question}' is not a valide conversion".format(question = self.raw_string))

    def normalize_measure(self, raw_measure, return_dimension):
        try:
            measure = ureg(raw_measure)
            return measure
        except UndefinedUnitError as err:
            self.error = "I don't know what is '{raw_measure}'".format(raw_measure=raw_measure)
            raise err

    def normalize_dimension(self, raw_dimension):
        for value in ureg._dimensions.values():
            if value.reference == raw_dimension:
                return value
        return raw_dimension


    def define_substance(self, raw_substance):
        try:
            if raw_substance:
                working_string = str(raw_substance)
                working_string.lower()
                working_string.strip()

                return sreg.get_density(working_string)
        except UnedfinedSubstanceError as err:
            self.error = "I don't know what is '{raw_substance}'".format(raw_substance=raw_substance)
            raise err


    def compute_response(self):
        try:
            source_unit = self.source_unit
            target_unit = self.target_unit

            if self.conversion_type == ConversionType.UsingDensity :
                density = self.substance.density * ureg.kilogram / (ureg.meter ** 3)
                return source_unit.to(target_unit, 'density', d = density)
            else:
                return source_unit.to(target_unit)

        except DimensionalityError as err:
            self.error = 'You can not convert {0} to {1}!'.format(self.source_dimension,self.target_dimension)
            raise err



def test():
    raw_string = "1 l to g"
    parser = PintParser(raw_string)

    print('The pretty representation is {:~P}'.format(parser.response))
    print(parser.raw_source_unit)
    print(parser.raw_target_unit)
    print(parser.source_unit)
    print(parser.target_unit)
    print(parser.raw_string)

if __name__ == '__main__':
    test()