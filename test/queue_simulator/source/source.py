from dynamic_system.dynamic_systems.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from models.core.base_model import ModelState
from models.models.discrete_event_model import DiscreteEventModel, ModelInput
from test.queue_simulator.source.properties.source_entity_type import SourceEntityType
from test.queue_simulator.source.properties.source_inter_arrival_time import SourceInterArrivalTime


# https://simulemos.cl/books/simio/page/source
from test.queue_simulator.source.properties.source_property_type import SourcePropertyType


class Source(DiscreteEventModel):
    def __init__(self,
                 dynamic_system: DiscreteEventDynamicSystem,
                 name: str,
                 entity_type: SourceEntityType = SourceEntityType(""),
                 inter_arrival_time: SourceInterArrivalTime = SourceInterArrivalTime(None)):
        super().__init__(dynamic_system, name, {
            'created_entities': 0
        }, {
            SourcePropertyType.SOURCE_ENTITY_TYPE: entity_type,
            SourcePropertyType.SOURCE_INTER_ARRIVAL_TIME: inter_arrival_time,
        })

    def __getInterArrivalTime(self) -> SourceInterArrivalTime:
        return self.getProperty(SourcePropertyType.SOURCE_INTER_ARRIVAL_TIME).getValue().evaluate()

    def _internalStateTransitionFunction(self, state: ModelState) -> ModelState:
        state['created_entities'] = self.__getInterArrivalTime()
        return state

    def _externalStateTransitionFunction(self, state: ModelState, inputs: ModelInput, event_time: float) -> ModelState:
        return state

    def _timeAdvanceFunction(self, state: ModelState) -> float:
        return 1

    def _outputFunction(self, state: ModelState) -> int:
        return state['created_entities']
