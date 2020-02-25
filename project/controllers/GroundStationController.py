# -*- coding: utf-8 -*-
from threading import Lock
from project import app, socketio
from flask import render_template, jsonify, request
from flask_socketio import SocketIO, join_room, emit, send, Namespace
from project.models.file_data import FlaskFileModel
from project.models.realtime_data import FlaskRealtimeModel
from werkzeug.utils import secure_filename
import os
import json
import datetime
import serial

PORT_NAME = "COM9"
BAUD_RATE = 115200
model = None
thread = None
thread_lock = Lock()
start_time = datetime.datetime.now()
ROOMS = {}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

def background_thread():
    """Example of how to send server generated events to clients."""
    socketio.sleep(2)
    count = 0
    with serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE, timeout=0.1) as ser:
        while True:
            socketio.sleep(0.3)
            # count += 1
            # data = realtime_model.get_recent_data()
            # socketio.sleep(10)
            # # print(data)

            try:
                data = {'acc': {'x': 0, 'y': 0, 'z': 0},
                        'magn': {'x': 0, 'y': 0, 'z': 0},
                        'gyro': {'x': 0, 'y': 0, 'z': 0},
                        'gps': {'lat': 0, 'lng': 0, 'h': 0}, 'time': ""}
                data_stream = ser.readline().decode("utf-8").replace("\r", "").replace("\n", "")
                # print(data_stream)
                data_stream = data_stream.split(",")
                if len(data_stream) == 13:
                    data['acc']['x'], data['acc']['y'], data['acc']['z'] = \
                        float(data_stream[0]), float(data_stream[1]), float(data_stream[2])
                    data['gyro']['x'], data['gyro']['y'], data['gyro']['z'] = \
                        float(data_stream[3]), float(data_stream[4]), float(data_stream[5])
                    data['magn']['x'], data['magn']['y'], data['magn']['z'] = \
                        float(data_stream[6]), float(data_stream[7]), float(data_stream[8])
                    data['gps']['lat'], data['gps']['lng'], data['gps']['h'] = \
                        float(data_stream[9]), float(data_stream[10]), float(data_stream[11])

                    # self.data['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
                    ms = (start_time.day * 24 * 60 * 60 + start_time.second) * 1000 + start_time.microsecond / 1000.0 + int(data_stream[12])
                    current_time = datetime.datetime.utcfromtimestamp(ms//1000).replace(microsecond=int(ms) % 1000*1000)

                    data['time'] = str(current_time.year) + "-" + str(current_time.month) + "-" + str(current_time.day) + " " + str(
                        current_time.hour) + ":" + str(current_time.minute) + ":" + str(current_time.second) + "." + str(current_time.microsecond)
                    graph_to_send = json.dumps(
                        ({'x': data['time'], 'y': data['acc']['x']},
                         {'x': data['time'], 'y': data['acc']['y']},
                         {'x': data['time'], 'y': data['acc']['z']},
                         {'x': data['time'], 'y': data['gyro']['x']},
                         {'x': data['time'], 'y': data['gyro']['y']},
                         {'x': data['time'], 'y': data['gyro']['z']},
                         {'x': data['time'], 'y': data['magn']['x']},
                         {'x': data['time'], 'y': data['magn']['y']},
                         {'x': data['time'], 'y': data['magn']['z']},
                         {'x': data['time'], 'y': data['gps']['lat']},
                         {'x': data['time'], 'y': data['gps']['lng']},
                         {'x': data['time'], 'y': data['gps']['h']}),
                    )
                    socketio.sleep(0)
                    socketio.emit('my_response', graph_to_send, namespace='/test')
            except UnicodeDecodeError as udc:
                pass

@app.route('/realtime', methods=['GET'])
def realtime():
    try:
        # model = FlaskRealtimeModel()
        pass
    except ModuleNotFoundError:
        return jsonify({"code": "model_error", "message": "Model was not found", "data": {"status": 404}})
    return render_template('data/realtime.html')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            # pass
            thread = socketio.start_background_task(background_thread)
    emit('connection', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


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


def allowed_filename(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


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
