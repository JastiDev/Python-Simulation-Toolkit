from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from core.debug.domain.debug import debug

if TYPE_CHECKING:
    from dynamic_system.discrete_events.models.discrete_event_model import (
        DiscreteEventModel,
    )


@dataclass
class ScheduledModel:
    """Event scheduled"""

    _model: DiscreteEventModel
    _time: float

    @debug("Getting the model")
    def getModel(self) -> DiscreteEventModel:
        """Gets the scheduled model."""
        return self._model

    @debug("Getting the time")
    def getTime(self) -> float:
        """Gets the time of the scheduled model."""
        return self._time

    @debug("Decreasing time")
    def decreaseTime(self, time: float) -> float:
        """Decreases the time for the scheduled model.

        Args:
            time (float): Time variation.
        """
        self._time = self._time - time
        return self._time

    def __lt__(self, other: ScheduledModel):
        return self._time < other._time

    def __eq__(self, other: ScheduledModel):
        return self._model == other._model
