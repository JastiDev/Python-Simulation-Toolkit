from typing import Any, Dict

from dynamic_system.models.discrete_event_dynamic_system import DiscreteEventDynamicSystem
from dynamic_system.models.discrete_event_model import DiscreteEventModel


class Drill(DiscreteEventModel):
    def __init__(self, dynamic_system: DiscreteEventDynamicSystem):
        super().__init__(dynamic_system, state={
            "p": 0,
            "s": 2
        }, name="Drill")

    def internalStateTransitionFunction(self, state: Dict[str, float]) -> Dict[str, float]:
        state["p"] = max(state["p"] - 1, 0)
        state["s"] = 2
        return state

    def externalStateTransitionFunction(self, state: Dict[str, float], parts: int, event_time: float) -> \
            Dict[str, float]:
        if state["p"] > 0:
            state["p"] = state["p"] + parts
            state["s"] = state["s"] - event_time
        elif state["p"] is 0:
            state["p"] = parts
            state["s"] = 2
            self._currentDynamicSystem.schedule(self, 2)
        return state

    def timeAdvanceFunction(self, state: Dict[str, float]) -> float:
        if state["p"] > 0:
            return state["s"]
        return 0

    def outputFunction(self, state: Dict[str, float]) -> int:
        if state["p"] > 0:
            return 1
        return 0

    def __str__(self):
        return "Drill -> s" + str(self._currentState)