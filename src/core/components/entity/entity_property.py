from __future__ import annotations

from typing import Any, Set, Type

from core.components.entity.property_type import PropertyType


class EntityProperty:
    """Property of an entity"""

    __name: str
    """Property name"""

    __value: Any
    """Property value"""

    __type: str
    """Property type"""

    def __init__(self, name: str,
                 value: Any = None,
                 property_type: str = PropertyType.STRING):
        self.__name = name
        self.__value = value
        self.__type = property_type

    def getName(self) -> str:
        """Returns the name of the property"""
        return self.__name

    def getType(self) -> str:
        """Returns the name of the property"""
        return self.__type

    def getValue(self) -> Any:
        """Returns the value of the property"""
        return self.__value

    def setValue(self, value):
        """Sets the value of the property"""
        if not PropertyType.validate(value, self.getType()):
            raise Exception("Expected " + self.getType() + "typing, but received " + type(value))
        self.__value = value

