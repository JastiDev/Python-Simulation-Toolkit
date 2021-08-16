from core.entity.core.entity_property import EntityProperty
from core.entity.core.property_type import PropertyType


class NumberProperty(EntityProperty):
    def __init__(self, value: float):
        super().__init__(value, PropertyType.NUMBER)

    def __add__(self, other):
        return NumberProperty(self.get_value() + other)

    def __sub__(self, other):
        return NumberProperty(self.get_value() - other)

    def __lt__(self, other):
        return self.get_value() < other

    def __gt__(self, other):
        return self.get_value() > other

    def __str__(self):
        return str(self.get_value())

    def get_value(self) -> float:
        """Returns the value of the property"""
        return super().get_value()
