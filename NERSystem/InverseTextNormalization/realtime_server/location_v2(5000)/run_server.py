#!/usr/bin/env python
import logging
import argparse
logging.basicConfig(level=logging.INFO)

from server import app

logger = logging.getLogger(__name__)

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "-p",
    "--port",
    help="Port to serve the server (default: 5000)",
    type=int,
    default=5000)

if __name__ == "__main__":
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler

    args = argparser.parse_args()
    port = args.port

    server = pywsgi.WSGIServer(('', port), app, handler_class=WebSocketHandler)
    logging.info(f"Serving server at port {port}")
    server.serve_forever()
    
 
