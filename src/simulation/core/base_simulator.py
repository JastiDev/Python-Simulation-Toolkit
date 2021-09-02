from __future__ import annotations

from abc import abstractmethod


from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem
from reports.core.base_report import BaseReport


class BaseSimulator:
    """Abstract simulator engine.

    An simulator engine executes the state transition function of the dynamic
    system, computes the output and reports it.
    """

    _dynamic_system: BaseDynamicSystem
    """Dynamic system to be simulated."""

    _is_output_up_to_update: bool
    """Indicates if the output was computed for that iteration."""

    _report_generator: BaseReport
    """Current report generator where engine saves the outputs."""

    def __init__(self, dynamic_system: BaseDynamicSystem, base_generator: BaseReport):
        """
        Args:
            dynamic_system (BaseDynamicSystem):
            base_generator (BaseReport):
        """
        self._dynamic_system = dynamic_system
        self._is_output_up_to_update = False
        self._report_generator = base_generator

    @abstractmethod
    def compute_next_state(self, *args, **kwargs):
        """Compute the next state of the dynamic system.

        Args:
            *args:
            **kwargs:
        """
        raise NotImplementedError

    @abstractmethod
    def compute_output(self):
        """Compute the output of the dynamic system if it has not computed
        yet
        """
        raise NotImplementedError
