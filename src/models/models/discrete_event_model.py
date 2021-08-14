from __future__ import annotations

from abc import abstractmethod
from typing import Any, Dict, cast

from core.components.entity.properties.expression_property import ExpressionProperty
from core.debug.domain.debug import debug
from mathematics.values.value import Value
from models.core.base_model import BaseModel, ModelState
from dynamic_system.dynamic_systems.discrete_event_dynamic_system import (
    DiscreteEventDynamicSystem,
)
from models.core.path import Path

ModelInput = Dict[str, Any]


class DiscreteEventModel(BaseModel):
    """DiscreteEventModel with an state"""

    def __init__(
            self,
            dynamic_system: DiscreteEventDynamicSystem,
            name: str = None,
            state: ModelState = None,
    ):
        """
        Args:
            dynamic_system (DiscreteEventDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
        """
        super().__init__(dynamic_system, name, state)
        # Add the model to the dynamic system
        self.schedule(self.get_time())

    @debug("Scheduling model")
    def schedule(self, time: float):
        """Schedules an autonomous event

        Args:
            time (float): Time when the event will be executed.
        """
        cast(DiscreteEventDynamicSystem, self.get_dynamic_system()).schedule(self, time)

    def add(self, model: DiscreteEventModel,
            weight: ExpressionProperty = ExpressionProperty(Value(1)),
            name: str = None) -> DiscreteEventModel:
        """Adds a model as an input for the current model in the dynamic system and returns the model added.

        Args:
            model (BaseModel): Output model to be added.
            weight (ExpressionProperty): Weight of the path.
            name (str): Name of the path.
        """
        return cast(DiscreteEventModel, super().add(model, weight, name))

    def add_path(self, path: Path) -> DiscreteEventModel:
        """Adds a path for the current model in the dynamic system and returns the model added.

        Args:
            path (Path): Connection to a model.
        """
        return cast(DiscreteEventModel, super().add_path(path))

    @debug("Getting time")
    def get_time(self) -> float:
        """Gets the time of the next autonomous event."""
        try:
            return self._time_advance_function(self.get_state())
        except AttributeError:
            return 0

    def get_output(self) -> Any:
        """Gets the output of the model."""
        return self._output_function(self.get_state())

    @debug("Executing state transition")
    def state_transition(self, inputs: ModelInput = None, event_time: float = 0):
        """Executes the state transition using the state given by the state
        transition function. If there are not inputs is an internal transition,
        otherwise it is an external transition.

        Args:
            inputs (ModelInput): Input trajectory x. If it is None, the state
                transition is autonomous
            event_time (float): Time of the event. If there are inputs and the
                time is ta(s), it is an confluent transition.
        """
        new_state: ModelState
        if inputs is None:
            # is an autonomous event
            new_state = self._internal_state_transition_function(self.get_state())
        elif event_time is self.get_time():
            # is an confluent event
            new_state = self._confluent_state_transition_function(self.get_state(), inputs)
        else:
            # time is between autonomous events, so it is an external event
            new_state = self._external_state_transition_function(
                self.get_state(), inputs, event_time
            )
        self.set_up_state(new_state)

    def _confluent_state_transition_function(
            self, state: ModelState, inputs: ModelInput
    ) -> ModelState:
        """
        .. math:: \delta_con(s,x)

        Implements the confluent state transition function delta. The
        confluent state transition executes an external transition function at
        the time of an autonomous event.

        .. math:: \delta_con \; : \; S \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
        """
        new_state = self._internal_state_transition_function(state)
        return self._external_state_transition_function(
            new_state, inputs, 0
        )  # 0 because is equal to (e = ta(s)) ½ ta(s)

    @abstractmethod
    def _internal_state_transition_function(self, state: ModelState) -> ModelState:
        """
        .. math:: \delta_int(s)

        Implements the internal state transition function delta. The internal
        state transition function takes the system from its state at the time of
        the autonomous event to a subsequent state.

        .. math:: \delta_int \; : \; S \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
        """
        raise NotImplementedError

    @abstractmethod
    def _external_state_transition_function(
            self, state: ModelState, inputs: ModelInput, event_time: float
    ) -> ModelState:
        """
        .. math:: \delta_ext((s,e), x)

        Implements the external state transition function delta. The external
        state transition function computes the next state of the model from its
        current total state (s,e) Q at time of an input and the input itself.

            .. math:: \delta_ext \; : \; Q \; x \; X \longrightarrow S

        Args:
            state (ModelState): Current state of the model.
            inputs (ModelInput): Input trajectory x.
            event_time (float): Time of event e.
        """
        raise NotImplementedError

    @abstractmethod
    def _time_advance_function(self, state: ModelState) -> float:
        """ta(s)

        Implement the model’s time advance function ta. The time advance
        function schedules output from the model and autonomous changes in its
        state.

        .. math:: ta \; : \; S \longrightarrow R_{0^\infty}

        Args:
            state (ModelState): Current state of the system.
        """
        raise NotImplementedError

    @abstractmethod
    def _output_function(self, state: ModelState) -> Any:
        """
        .. math:: \lambda \; (s)

        Implements the output function lambda. The output function describes
        how the state of the system appears to an observer when e=ta(s).

        .. math:: \lambda \; : \; S \; \longrightarrow Y

        Args:
            state (ModelState): current state s of the model.
        """
        raise NotImplementedError
