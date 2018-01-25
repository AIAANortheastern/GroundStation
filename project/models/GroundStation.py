import threading
import serial
import json
import time
import math
import os

# Please note that this port name will have to be changed as necessary depending on what port the xbee is
# connected to.
PORT_NAME = None
DATA_HEADER = 'A'

# in bytes
DATA_LEN = 32


class FlaskModel:
    data = dict()

    def __init__(self, port=None):
        # csv structure 'timestamp,altitude,pressure,temperature,gyrox,gyroy,gyroz,magx,magy,magz,rhall\n'
        self.data = {'timestamp': time.strftime("%Y,%m,%d,%H:%M:%S"), 'altitude': 0, 'pressure': None,
                     'temperature': None, 'gyrox': None, 'gyroy': None, 'gyroz': None, 'magx': None, 'magy': None,
                     'magz': None, 'longitude': None, 'latitude': None, 'rhall': None, 'slider_pos': 0}
# {'alti': {'temp': 0, 'press': 0, 'altitude': 0}, 'magn': {'x': 0, 'y': 0, 'z': 0, 'rhall': 0},
#                   'gyro': {'x': 0, 'y': 0, 'z': 0}}
        self.threads_ok = True
        self.filename = 'AvionicsData.csv'
        global PORT_NAME
        PORT_NAME = port
        if PORT_NAME is not None:
            data_thread = threading.Thread(target=self._get_data_from_radio())
            data_thread.start()
        else:
            self.data_pos = dict()
            with open(self.filename, 'r') as f:
                first_line = f.readline()
                for key, data in self.data.items():
                    # for each key figure out what order it is in in the file.
                    try:
                        self.data_pos[key] = first_line.split(',').index(key)
                    except ValueError:
                        self.data_pos[key] = -1



            # load the data from the file to start parsing through it

        # radio_thread = threading.Thread(target=self._radio_input_to_file)
        # radio_thread.start()

    # def _get_data(self):
    #     # This function is going to go ahead and read data out from the json file.
    #
    #     while self.threads_ok:
    #         # do magical reading from json
    #         pass

    def _get_data_from_radio(self):
        try:
            with serial.Serial(PORT_NAME, 9600) as ser:
                while self.threads_ok:
                    try:
                        while ser.read(1).decode('UTF-8') != DATA_HEADER:
                             # keep doing the read until you get to the beginning of the data stream
                             pass

                        data_stream = ser.read(DATA_LEN - len(DATA_HEADER))
                        # bytearray.fromhex('2B09000077830100C31F000010000000BD7F0000CD180000AFFF200300020A')

                        self.data['alti']['temp'], self.data['alti']['press'] = \
                            int.from_bytes(data_stream[0:4], byteorder='little'), \
                            int.from_bytes(data_stream[4:8], byteorder='little')

                        current_press = self.data['alti']['press']
                        if current_press != 0:
                            self.data['alti']['altitude'] = math.log(101760.98/current_press)

                        self.data['magn']['x'], self.data['magn']['y'], self.data['magn']['z'], self.data['magn']['rhall'] = \
                            int.from_bytes(data_stream[8:12], byteorder='little'), \
                            int.from_bytes(data_stream[12:16], byteorder='little'), \
                            int.from_bytes(data_stream[16:20], byteorder='little'), \
                            int.from_bytes(data_stream[20:24], byteorder='little')

                        self.data['gyro']['x'], self.data['gyro']['y'], self.data['gyro']['z'] = \
                            int.from_bytes(data_stream[24:26], byteorder='little'), \
                            int.from_bytes(data_stream[26:28], byteorder='little'), \
                            int.from_bytes(data_stream[28:30], byteorder='little')

                        time_str = time.strftime("%Y,%m,%d,%H:%M:%S")

                        with open(self.filename, "r") as json_file:
                            json_data = json.load(json_file)
                        json_data['data'][time_str] = self.data
                        json_str = json.dumps(json_data)
                        with open(self.filename, "w") as json_file:
                            json_file.write(json_str)
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
        except Exception as e:
            print(e)
            self.kill_threads()
            raise ValueError("Failed to Connect to port {0}".format(PORT_NAME))

    def get_first_line_data(self):
        with open(self.filename, "rb") as f:
            first = f.readline()  # Read the first line.
            self.get_data_from_csv_line(first)
            return self.data

    def get_next_line_data(self):
        pass

    def get_prev_line_data(self):
        pass

    def get_value_with_slider(self, slider_val):
        pass

    def get_recent_data(self):
        # Read the last line of the file efficiently
        # https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file
        with open(self.filename, "rb") as f:
            first = f.readline()  # Read the first line.
            f.seek(-2, os.SEEK_END)  # Jump to the second last byte.
            while f.read(1) != b"\n":  # Until EOL is found...
                f.seek(-2, os.SEEK_CUR)  # ...jump back the read byte plus one more.
            last = f.readline().decode('utf-8')  # Read last line.
            self.get_data_from_csv_line(last)
            self.data['slider_pos'] = 1000
            return self.data

    def get_data_from_csv_line(self, line):
        # use the self.data_pos structure to properly read data values in the correct order.
        array = line.split(',')
        for key, value in self.data.items():
            self.data[key] = array[self.data_pos[key]]

    def kill_threads(self):
        self.threads_ok = False
