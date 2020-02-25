# -*- coding: utf-8 -*-
__version__ = '0.1'
import os
from flask import Flask
from flask_socketio import SocketIO
import eventlet
eventlet.monkey_patch()

app = Flask(__name__)
async_mode = "eventlet"
socketio = SocketIO(app, async_mode=async_mode, debug=True,ping_interval=5, ping_timeout=30)

port = int(os.environ.get('PORT', 5000))
app.config['SECRET_KEY'] = 'secret!'

UPLOAD_FOLDER = "upload\\csv"
ALLOWED_EXTENSIONS = {'csv', 'txt'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
# toolbar = DebugToolbarExtension(app)
from project.controllers import *
