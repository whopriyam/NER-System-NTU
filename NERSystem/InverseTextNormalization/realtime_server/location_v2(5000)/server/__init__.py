from flask import Flask, Blueprint
from flask_sockets import Sockets

from server.blueprints.ws import ws

app = Flask(__name__)
sockets = Sockets(app)

sockets.register_blueprint(ws, url_prefix=r'/')
