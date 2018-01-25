# -*- coding: utf-8 -*-
from project import app
from flask import render_template
from project.models.GroundStation import FlaskModel
from flask import jsonify

model = None


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/data-main', methods=['GET'])
def data():
    global model
    model = FlaskModel()
    return render_template('data/data-main.html', data=model.data)


# This should only be called via ajax when you are already in the /data-main page so it
# is ok we rely on the model
@app.route('/data-recent/', methods=['GET'])
def data_recent():
    global model
    ret_data = model.get_recent_data()
    return jsonify(ret_data)


@app.route('/data-first/', methods=['GET'])
def data_first():
    global model
    ret_data = model.get_first_line_data()
    return jsonify(ret_data)