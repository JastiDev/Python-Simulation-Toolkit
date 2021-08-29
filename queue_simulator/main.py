from typing import List, Dict

import eventlet
import socketio

from loguru import logger
from experiments.experiment_builders import DiscreteEventExperiment
from queue_simulator.shared.dynamic_systems import SimulationDynamicSystem
from queue_simulator.shared.nodes import NodeType, NodeBuilder

sio = socketio.Server(cors_allowed_origins='*')
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

serial = 0


@sio.event
def connect(sid, environ):
    logger.info("Client connected: {sid}", sid=sid)
    session: Dict[str, DiscreteEventExperiment]
    with sio.session(sid) as session:
        session['experiment'] = DiscreteEventExperiment(SimulationDynamicSystem())


@sio.event
def create_node(sid, data: Dict[str, NodeType]):
    node = data['node']
    logger.info("Create node: {node}, sid: {sid}", node=node, sid=sid)
    session: Dict[str, DiscreteEventExperiment]
    with sio.session(sid) as session:
        ds = session['experiment'].dynamic_system
        created_node = NodeBuilder.create_node(node, ds)
    return created_node.serialize()

@sio.event
def disconnect(sid):
    print('disconnect ', sid)


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('localhost', 4000)), app)
