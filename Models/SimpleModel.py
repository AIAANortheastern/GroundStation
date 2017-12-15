import threading
import random
import serial
import json
import time

# Please note that this port name will have to be changed as necessary depending on what port the xbee is
# connected to.
PORT_NAME = 'COM3'
DATA_HEADER = 'A'

# in bytes
DATA_LEN = 32


class SimpleModel:
    data = dict()

    def __init__(self):
        self.data = self.data = {'alti': {'temp': 0, 'press': 0}, 'magn': {'x': 0, 'y': 0, 'z': 0, 'rhall': 0},
                                 'gyro': {'x': 0, 'y': 0, 'z': 0}}
        self.threads_ok = True
        self.filename = 'AvionicsData.json'
        data_thread = threading.Thread(target=self._get_data)
        data_thread.start()

        # radio_thread = threading.Thread(target=self._radio_input_to_file)
        # radio_thread.start()

    # def _get_data(self):
    #     # This function is going to go ahead and read data out from the json file.
    #
    #     while self.threads_ok:
    #         # do magical reading from json
    #         pass

    def _get_data(self):
        try:
          #  with serial.Serial(PORT_NAME, 9600) as ser:
            while self.threads_ok:
                try:
                    # while ser.read(1).decode('UTF-8') != DATA_HEADER:
                    #     # keep doing the read until you get to the beginning of the data stream
                    #     pass
                    data_stream = bytearray.fromhex('2B09000077830100C31F000010000000BD7F0000CD180000AFFF200300020A')
                    # ser.read(DATA_LEN - len(DATA_HEADER))
                    self.data['alti']['temp'], self.data['alti']['press'] = \
                        int.from_bytes(data_stream[0:4], byteorder='little'), \
                        int.from_bytes(data_stream[4:8], byteorder='little')

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

    def kill_threads(self):
        self.threads_ok = False
