from __future__ import annotations

from core.components.entity.core.entity_property import EntityProperty
from core.components.entity.core.property_type import PropertyType
from core.components.expresions.expression import Expression
from queue_simulator.source.properties.source_property_type import SourceProperty


class SourceInterArrivalTime(EntityProperty):
    def __init__(self, time: Expression = None):
        super().__init__(SourceProperty.SOURCE_INTER_ARRIVAL_TIME,
                         time, PropertyType.EXPRESSION)

    def getValue(self) -> Expression:
        """Returns the value of the property"""
        return super(SourceInterArrivalTime, self).getValue()
