from __future__ import annotations

from abc import abstractmethod
from typing import Any, Set, TYPE_CHECKING, cast


from core.debug.domain.debug import debug
from core.entity.core.entity import Entity
from core.entity.properties.expression_property import ExpressionProperty
from core.mathematics.values.value import Value
from models.core.path import Path

if TYPE_CHECKING:
    from dynamic_system.core.base_dynamic_sytem import BaseDynamicSystem

ModelState = Any


class BaseModel(Entity):
    """Base model in a dynamic system"""

    _serial_id = 0
    """Serial of the model"""

    __current_dynamic_system: BaseDynamicSystem
    """Current dynamic system of the model"""

    __current_state: ModelState
    """Current state of the model"""

    @debug("Initialized Model", True)
    def __init__(self, dynamic_system: BaseDynamicSystem, name: str = None,
                 state: ModelState = None):
        """
        Args:
            dynamic_system (BaseDynamicSystem): Dynamic system of the
                model.
            name (str): Name of the model.
            state (ModelState): Initial state of the model.
        """
        # Init the model
        if name is None:
            super().__init__("model" + str(BaseModel._serial_id))
            BaseModel._serial_id = BaseModel._serial_id + 1
        else:
            super().__init__(name)
        self.set_up_state(state)
        self.__output_models = set()
        # Set dynamic system
        self.__current_dynamic_system = dynamic_system
        self.__current_dynamic_system.add(self)

    @debug("Setting up the state")
    def set_up_state(self, state: ModelState):
        """s

        Sets up the state of the model.

        Args:
            state (ModelState): New state of the model.
        """
        self.__current_state = state

    @debug("Getting the state")
    def get_state(self) -> ModelState:
        """Returns the current state"""
        return self.__current_state

    @debug("Adding output")
    def add(self, model: BaseModel,
            weight: ExpressionProperty = ExpressionProperty(Value(1)),
            name: str = None):
        """Adds a model as an input for the current model in the dynamic system and returns the model added.
        
        Args:
            model (BaseModel): Output model to be added.
            weight (ExpressionProperty): Weight of the path.
            name (str): Name of the path.
        """
        return self.add_path(Path(model, weight, name))

    @debug("Adding path")
    def add_path(self, path: Path):
        """Adds a path for the current model in the dynamic system and returns the model added.

        Args:
            path (Path): Connection to a model.
        """
        self.__current_dynamic_system.add(path.get_source_model())
        self.__output_models.add(path)
        return path.get_source_model()

    @debug("Removing output")
    def remove(self, model: BaseModel):
        """Removes an specified output

        Args:
            model (BaseModel): Model to be removed.
        """
        if model in self.__output_models:
            self.__output_models.remove(cast(Any, model))

    @debug("Getting output models")
    def get_output_models(self) -> Set[Path]:
        """Returns the output models of the current model"""
        return self.__output_models

    @debug("Retrieving dynamic system")
    def get_dynamic_system(self) -> BaseDynamicSystem:
        """Returns the dynamic system where the current model belongs with"""
        return self.__current_dynamic_system

    @abstractmethod
    def get_output(self) -> Any:
        """Gets the output of the model."""
        raise NotImplementedError

    @abstractmethod
    def state_transition(self, *args, **kwargs):
        """Executes the state transition function"""
        raise NotImplementedError

    def __str__(self):
        name = self.get_id()
        state = self.get_state()
        return name + ": {'state': " + str(state) + "}"
