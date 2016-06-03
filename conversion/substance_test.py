from conversion.substance import *

registry = SubstanceRegistry()

print(registry.get_density("corn"))
print(registry._substances)