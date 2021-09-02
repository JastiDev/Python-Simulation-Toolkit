import unittest
from decimal import Decimal

from core.entity.core import Entity
from core.entity.properties import ExpressionProperty
from core.mathematics.values.value import Value
from dynamic_system.future_event_list import Scheduler
from experiments.experiment_builders import DiscreteEventExperiment
from models.core import Path
from test.mocks.dynamic_system_mock import DynamicSystemMock
from test.mocks.model_mock import ModelMock


class DiscreteEventExperimentTest(unittest.TestCase):
    """Test discrete event experiments"""

    experiment: DiscreteEventExperiment
    """experiment to be tested"""

    def setUp(self) -> None:
        """Sets up tests"""
        dynamic_system = DynamicSystemMock(Scheduler())
        self.experiment = DiscreteEventExperiment(dynamic_system)

    def tearDown(self) -> None:
        """Remove changes of the tests."""
        Entity._saved_names = set()

    def test_save_and_load(self):
        m1 = ModelMock(self.experiment.dynamic_system)
        m2 = ModelMock(self.experiment.dynamic_system)

        m1.set_up_state(5)
        m2.set_up_state(10)

        self.experiment.dynamic_system.schedule(m1, Decimal(10))

        m12 = Path(m1, m2, ExpressionProperty(Value(1)))

        self.experiment.dynamic_system.link(m12)

        data = self.experiment.save()
        loaded_experiment = self.experiment.load(data)

        models_expected = set(
            [m.get_id() for m in self.experiment.dynamic_system._models]
        )
        models_actual = set(
            m.get_id() for m in loaded_experiment.dynamic_system._models
        )

        paths_expected = set(m.get_id() for m in self.experiment.dynamic_system._paths)
        paths_actual = set(m.get_id() for m in loaded_experiment.dynamic_system._paths)

        self.assertEqual(models_expected, models_actual)
        self.assertEqual(paths_expected, paths_actual)


if __name__ == "__main__":
    unittest.main()
