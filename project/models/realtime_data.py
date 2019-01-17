import threading
import serial
import json
import time
import math
import os
import mmap
import linecache
from os import walk
from pathlib import Path
# Please note that this port name will have to be changed as necessary depending on what port the xbee is
# connected to.
PORT_NAME = None
DATA_HEADER = 'A'

# in bytes
DATA_LEN = 32


class FlaskRealtimeModel:
    data = dict()

    def __init__(self, port="COM9"):
        # csv structure 'timestamp,altitude,pressure,temperature,gyrox,gyroy,gyroz,magx,magy,magz,rhall\n'
        # self.data = {'timestamp': time.strftime("%Y,%m,%d,%H:%M:%S"), 'altitude': 0, 'pressure': None,
        #                 'temperature': None, 'gyrox': None, 'gyroy': None, 'gyroz': None, 'magx': None, 'magy': None,
        #                'magz': None, 'longitude': None, 'latitude': None, 'rhall': None, 'slider_pos': 0}

        # {'alti': {'temp': 0, 'press': 0, 'altitude': 0}, 'magn': {'x': 0, 'y': 0, 'z': 0, 'rhall': 0},
        #                   'gyro': {'x': 0, 'y': 0, 'z': 0}}
        self.data = {'acc': {'x': 0, 'y': 0, 'z': 0},
                     'magn': {'x': 0, 'y': 0, 'z': 0},
                     'gyro': {'x': 0, 'y': 0, 'z': 0}}
        self.threads_ok = True
        self.filename = 'upload\\json\\realtime.json'
        global PORT_NAME
        PORT_NAME = port
        if PORT_NAME is not None:
            data_thread = threading.Thread(target=self._get_data_from_radio())
            data_thread.start()

        # load the data from the file to start parsing through it

        # radio_thread = threading.Thread(target=self._radio_input_to_file)
        # radio_thread.start()

    # def _get_data(self):
    #     # This function is going to go ahead and read data out from the json file.
    #
    #     while self.threads_ok:
    #         # do magical reading from json
    #         pass

    # RADIO data functions
    def _get_data_from_radio(self):
        # try:
            with serial.Serial(port=PORT_NAME,
                               baudrate=115200) as ser:
                while self.threads_ok:
                    try:
                        #
                        #     while ser.read(1).decode('UTF-8') != DATA_HEADER:
                        #             # keep doing the read until you get to the beginning of the data stream
                        #         pass
                        #
                        data_stream = ser.readline().decode("utf-8").replace("\r", "").replace("\n", "")
                        data_stream = data_stream.split(",")
                        # print(data_stream)
                    #     # bytearray.fromhex('2B09000077830100C31F000010000000BD7F0000CD180000AFFF200300020A')
                    #
                    #    self.data['alti']['temp'], self.data['alti']['press'] = \
                    #       int.from_bytes(data_stream[0:4], byteorder='little'), \
                    #       int.from_bytes(data_stream[4:8], byteorder='little')
                    #
                    #     current_press = self.data['alti']['press']
                    #     if current_press != 0:
                    #         self.data['alti']['altitude'] = math.log(101760.98/current_press)
                    #
                        self.data['acc']['x'], self.data['acc']['y'], self.data['acc']['z'] = \
                            float(data_stream[0]), float(data_stream[1]), float(data_stream[2])

                        self.data['magn']['x'], self.data['magn']['y'], self.data['magn']['z'] = \
                            float(data_stream[3]), float(data_stream[4]), float(data_stream[5])

                        self.data['gyro']['x'], self.data['gyro']['y'], self.data['gyro']['z'] = \
                            float(data_stream[6]), float(data_stream[7]), float(data_stream[8])

                        time_str = time.strftime("%Y,%m,%d,%H:%M:%S")
                        #print(self.data)

                        # with open(self.filename, "r") as json_file:
                        #     json_data = json.load(json_file)
                        # json_data['data'][time_str] = self.data
                        # json_str = json.dumps(json_data)
                        # with open(self.filename, "w") as json_file:
                        #     json_file.write(json_str)

                    except UnicodeDecodeError as udc:
                        pass
                    # Hey the read for the header got a number
                    except FileNotFoundError as file_error:
                        time_str = time.strftime("%Y,%m,%d,%H:%M:%S")
                        json_data = {'data': {}}
                        json_data['data'][time_str] = self.data
                        json_str = json.dumps(json_data)
                        with open(self.filename, "w") as json_file:
                            json_file.write(json_str)
        # except Exception as e:
        #     print(e)
        #     self.kill_threads()
        #     raise ValueError("Failed to Connect to port {0}".format(PORT_NAME))

    def kill_threads(self):
        self.threads_ok = False
