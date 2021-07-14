from __future__ import annotations

from core.components.entity.core.entity_property import EntityProperty
from queue_simulator.source.properties.source_property_type import SourceProperty


class SourceEntityType(EntityProperty):
    def __init__(self, entity_name: str = None):
        super().__init__(SourceProperty.SOURCE_ENTITY_TYPE,
                         entity_name)

    def getValue(self) -> str:
        """Returns the value of the property"""
        return super(SourceEntityType, self).getValue()
