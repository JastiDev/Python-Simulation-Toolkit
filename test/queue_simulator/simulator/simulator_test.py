import unittest

from core.entity.properties import Property, NumberProperty
from core.mathematics.values.value import Value
from core.types import Time
from queue_simulator.buffer.core import BufferProperty
from queue_simulator.label.label import Label
from queue_simulator.shared.experiments.simulation_experiment import SimulationExperiment
from queue_simulator.shared.nodes import NodeType


class SimulatorTest(unittest.TestCase):
    """Base dynamic system tests"""
    experiment: SimulationExperiment

    def setUp(self) -> None:
        """Sets up tests"""
        self.experiment = SimulationExperiment()

    def test_basic_simulation(self):
        """1 source, 1 server, 1 arrival/second every second during 5 seconds"""
        emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
        source = self.experiment.add_node(NodeType.SOURCE)
        source.set_id("Source")
        source.entity_emitter = Property(emitter)
        source.inter_arrival_time = Value(1)
        source.entities_per_arrival = Value(1)
        source.time_offset = Value(0)

        server = self.experiment.add_node(NodeType.SERVER)
        server.set_id("Server")
        server.processing_time = Value(1)

        sink = self.experiment.add_node(NodeType.SINK)
        sink.set_id("Sink")

        source.add(server)
        server.add(sink)

        source.init()

        label_source_out = Label(source.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_in = Label(server.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_out = Label(server.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_sink_in = Label(sink.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)

        self.experiment.simulation_control.start(stop_time=Time(5))
        self.experiment.simulation_control.wait()
        self.experiment.save()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))

        print(self.experiment.simulation_report.generate_report())

        self.assertEqual("6", str(label_source_out))
        self.assertEqual("5", str(label_server_in))
        self.assertEqual("4", str(label_server_out))
        self.assertEqual("4", str(label_server_out))

    def test_simulation_server_delay(self):
        """Server process entities slowly than arrivals"""
        emitter = self.experiment.add_node(NodeType.ENTITY_EMITTER)
        source = self.experiment.add_node(NodeType.SOURCE)
        source.set_id("Source")
        source.entity_emitter = Property(emitter)
        source.inter_arrival_time = Value(1)
        source.entities_per_arrival = Value(2)
        source.time_offset = Value(0)

        server = self.experiment.add_node(NodeType.SERVER)
        server.set_id("Server")
        server.processing_time = Value(2)
        server.initial_capacity = NumberProperty(1000)

        sink = self.experiment.add_node(NodeType.SINK)
        sink.set_id("Sink")

        source.add(server)
        server.add(sink)

        source.init()

        label_source_out = Label(source.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_in = Label(server.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_server_out = Label(server.get_state().output_buffer.get_properties, BufferProperty.NUMBER_ENTERED)
        label_sink_in = Label(sink.get_state().input_buffer.get_properties, BufferProperty.NUMBER_ENTERED)

        self.experiment.save()

        self.experiment.simulation_control.start(stop_time=Time(10))
        self.experiment.simulation_control.wait()

        print("Generated: " + str(label_source_out))
        print("Entered to server: " + str(label_server_in))
        print("Processed by server: " + str(label_server_out))
        print("Entered to sink: " + str(label_sink_in))
        print(self.experiment.simulation_report.generate_report())

        self.assertEqual("22", str(label_source_out))
        self.assertEqual("20", str(label_server_in))
        self.assertEqual("16", str(label_server_out))
        self.assertEqual("16", str(label_server_out))


if __name__ == '__main__':
    unittest.main()
