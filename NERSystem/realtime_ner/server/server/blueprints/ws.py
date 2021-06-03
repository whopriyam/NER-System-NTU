import json
import logging
from flask import Blueprint

# from server.segment_text import segment_flight_number, segment_text, segment_text_neural
from server.annotate import annotate

logger = logging.getLogger(__name__)

ws = Blueprint(r'ws', __name__)


@ws.route('/')
def segment(socket):
    while not socket.closed:
        message = socket.receive()
        logger.debug(message)
        socket.send(annotate(message))


