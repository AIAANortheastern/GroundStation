# -*- coding: utf-8 -*-
from project import app
from flask import render_template
from project.models.GroundStation import FlaskModel
from flask import jsonify, request

model = None


@app.route('/')
def start():
    return render_template('index.html')


@app.route('/data-main', methods=['GET'])
def data():
    global model
    try:
        model = FlaskModel()
    except ModuleNotFoundError:
        pass
    return render_template('data/data-main.html', data=model.data)


# This should only be called via ajax when you are already in the /data-main page so it
# is ok we rely on the model
@app.route('/data-recent/', methods=['GET'])
def data_recent():
    try:
        model = FlaskModel()
    except ModuleNotFoundError:
        pass
    ret_data = model.get_recent_data()
    return jsonify(ret_data)


@app.route('/data-first/', methods=['GET'])
def data_first():
    try:
        model = FlaskModel()
    except ModuleNotFoundError:
        pass
    ret_data = model.get_first_line_data()
    return jsonify(ret_data)

@app.route('/data-length/', methods=['GET'])
def data_length():
    try:
        model = FlaskModel()
    except ModuleNotFoundError:
        pass
    ret_data = model.data_length()
    return jsonify(ret_data)

@app.route('/data-range/', methods=['GET'])
def data_range():
    try:
        model = FlaskModel()
    except ModuleNotFoundError:
        pass
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    if (start < 1) or (end <= start) or (end > model.file_length):
        error_message = 'START/END OUT OF RANGE'
        return jsonify({"code":"invalid_num","message":"Arguments were out of range or incorrect","data":{"status":404}})

    ret_data = model.get_data_in_range(start, end)
    return jsonify(ret_data)