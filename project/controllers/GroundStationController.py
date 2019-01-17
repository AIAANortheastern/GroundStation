# -*- coding: utf-8 -*-
from project import app
from flask import render_template, jsonify, request
from project.models.file_data import FlaskFileModel
from project.models.realtime_data import FlaskRealtimeModel
from werkzeug.utils import secure_filename
import os
import asyncio
import websockets
import datetime
import random


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


model = None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, '127.0.0.1', 5678)



@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        # model = FlaskRealtimeModel()
        pass
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    return render_template('data/realtime.html')





@app.route('/upload', methods=['GET'])
def get_upload():
    return render_template('data/upload.html')


@app.route('/upload', methods=['POST'])
def post_upload():
    submitted_file = request.files['csv']
    if submitted_file and allowed_filename(submitted_file.filename):
        filename = secure_filename(submitted_file.filename)
        submitted_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('data/upload.html', success=True)
    return render_template('data/upload.html', success=False)


@app.route('/select-columns', methods=['GET'])
def select_column():
    return render_template('data/column-selection.html')


@app.route('/available-files', methods=['GET'])
def show_files():
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return jsonify(model.query_uploaded_files())


@app.route('/data-selection', methods=['GET'])
def select_data():
    global model
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return render_template('data/data-selection.html', data=model.data)


async def time(websocket, path):
    while True:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        await websocket.send(now)
        await asyncio.sleep(random.random() * 3)

start_server = websockets.serve(time, '127.0.0.1', 5678)


@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        # model = FlaskRealtimeModel()
        pass
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
    return render_template('data/realtime.html')





@app.route('/upload', methods=['GET'])
def get_upload():
    return render_template('data/upload.html')


@app.route('/upload', methods=['POST'])
def post_upload():
    submitted_file = request.files['csv']
    if submitted_file and allowed_filename(submitted_file.filename):
        filename = secure_filename(submitted_file.filename)
        submitted_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template('data/upload.html', success=True)
    return render_template('data/upload.html', success=False)


@app.route('/select-columns', methods=['GET'])
def select_column():
    return render_template('data/column-selection.html')


@app.route('/available-files', methods=['GET'])
def show_files():
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return jsonify(model.query_uploaded_files())


@app.route('/data-selection', methods=['GET'])
def select_data():
    global model
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return render_template('data/data-selection.html', data=model.data)


@app.route('/data-main', methods=['GET'])
def start():
    global model
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return render_template('data/data-main.html', data=model.data)


# This should only be called via ajax when you are already in the /data-main page so it
# is ok we rely on the model
@app.route('/data-recent/', methods=['GET'])
def data_recent():
    global model
    try:
        if model is None:
            raise ModuleNotFoundError
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    filename = request.args.get('filename')
    ret_data = model.get_recent_data(filename)
    return jsonify(ret_data)


@app.route('/data-first/', methods=['GET'])
def data_first():
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    filename = request.args.get('filename')
    ret_data = model.get_first_line_data(filename)
    return jsonify(ret_data)


@app.route('/data-length/', methods=['GET'])
def data_length():
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    filename = request.args.get('filename')
    ret_data = model.data_length(filename)
    return jsonify(ret_data)


@app.route('/data-range/', methods=['GET'])
def data_range():
    global model
    try:
        model = FlaskFileModel()
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    filename = request.args.get('filename')

    ret_data = model.get_data_in_range(filename, start, end)
    if ret_data == "error":
        return jsonify({"code": "invalid_num",
                 "message": "Arguments were out of range or incorrect",
                 "data": {"status": 404}})
    return jsonify(ret_data)
