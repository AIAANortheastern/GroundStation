# -*- coding: utf-8 -*-
__version__ = '0.1'
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension


UPLOAD_FOLDER = "upload\\csv"
ALLOWED_EXTENSIONS = {'csv', 'txt'}

app = Flask('project')
app.config['SECRET_KEY'] = 'random'
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
toolbar = DebugToolbarExtension(app)
from project.controllers import *
