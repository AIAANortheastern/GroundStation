
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


class FlaskFileModel:
    data = dict()

    def __init__(self, port="COM9"):
        # csv structure 'timestamp,altitude,pressure,temperature,gyrox,gyroy,gyroz,magx,magy,magz,rhall\n'
        # self.data = {'timestamp': time.strftime("%Y,%m,%d,%H:%M:%S"), 'altitude': 0, 'pressure': None,
        #                 'temperature': None, 'gyrox': None, 'gyroy': None, 'gyroz': None, 'magx': None, 'magy': None,
        #                'magz': None, 'longitude': None, 'latitude': None, 'rhall': None, 'slider_pos': 0}
        # {'alti': {'temp': 0, 'press': 0, 'altitude': 0}, 'magn': {'x': 0, 'y': 0, 'z': 0, 'rhall': 0},
        #                   'gyro': {'x': 0, 'y': 0, 'z': 0}}
        self.threads_ok = True
        # self.filename = 'upload\\csv\\AvionicsData.csv'
        self.upload_folder = 'upload\\csv\\'


        # self.file_length = self.data_length()
        self.data_pos = dict()
        # with open(self.filename, 'r') as f:
        #     first_line = f.readline()
        #     for key, data in self.data.items():
        #         # for each key figure out what order it is in in the file.
        #         self.array = first_line.split(',');
        #         try:
        #             self.data_pos[key] = self.array.index(key)
        #         except ValueError:
        #             self.data_pos[key] = -1

        # load the data from the file to start parsing through it

        # radio_thread = threading.Thread(target=self._radio_input_to_file)
        # radio_thread.start()

    # def _get_data(self):
    #     # This function is going to go ahead and read data out from the json file.
    #
    #     while self.threads_ok:
    #         # do magical reading from json
    #         pass

    # FILE data functions


    def query_uploaded_files(self):
        f = []
        for (dirpath, dirnames, filenames) in walk(self.upload_folder):
            f.extend(filenames)
            break
        return f

    def check_if_file_exists(self, filename):
        my_file = Path(self.upload_folder+filename)
        return my_file.is_file()

    def get_first_line_data(self, filename):
        if self.check_if_file_exists(filename):
            with open(filename, "rb") as f:
                first = f.readline()  # Read the first line.
                self.get_data_from_csv_line(first.decode('utf-8'))
                return self.data

    def get_recent_data(self, filename):
        # Read the last line of the file efficiently
        # https://stackoverflow.com/questions/3346430/what-is-the-most-efficient-way-to-get-first-and-last-line-of-a-text-file
        if self.check_if_file_exists(filename):
            with open(filename, "rb") as f:
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
        line = line.split("\n")[0]
        # gets rid of \n character
        array = line.split(',')
        for key, value in self.data.items():
            if value == -1:
                continue
            else:
                self.data[key] = array[self.data_pos[key]]
        return array

    def get_data_in_range(self, filename, start, stop): #error catching must be in controller
        if self.check_if_file_exists(filename):
            if (start < 1) or (stop <= start) or (stop > self.data_length(filename)):
                return "error"
            array = []
            for x in range(start, stop):
                array.append(linecache.getline(os.path.abspath(self.upload_folder+filename), x))
                array[x-start] = self.get_data_from_csv_line(array[x-start])
            linecache.clearcache()
            return array
        return "error"

    def data_length(self, filename):
        if self.check_if_file_exists(filename):
            with open(self.upload_folder+filename, "r+") as f:
                buf = mmap.mmap(f.fileno(), 0)
                lines = 0
                read_line = buf.readline
                while read_line():
                    lines += 1
                return lines

    def kill_threads(self):
        self.threads_ok = False
