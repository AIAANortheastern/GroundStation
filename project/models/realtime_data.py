import threading, serial, json, time, ast, math, os, mmap, linecache, datetime
from pathlib import Path
# Please note that this port name will have to be changed as necessary depending on what port the xbee is
# connected to.
PORT_NAME = None
DATA_HEADER = 'A'

# in bytes
DATA_LEN = 32
PORT_NAME = "COM4"
BAUD_RATE = 115200


class FlaskRealtimeModel:
    data = dict()

    def __init__(self):
        # csv structure 'timestamp,altitude,pressure,temperature,gyrox,gyroy,gyroz,magx,magy,magz,rhall\n'

        self.data = {'acc': {'x': 0, 'y': 0, 'z': 0},
                     'magn': {'x': 0, 'y': 0, 'z': 0},
                     'gyro': {'x': 0, 'y': 0, 'z': 0}, 'time': ""}
        self.threads_ok = True
        self.filename = 'upload\\json\\realtime.json'

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
        try:
            with serial.Serial(port=PORT_NAME, baudrate=BAUD_RATE) as ser:
                while self.threads_ok:
                    try:

                        data_stream = ser.readline().decode("utf-8").replace("\r", "").replace("\n", "")
                        # print(data_stream)
                        data_stream = data_stream.split(",")
                        if len(data_stream) == 10:
                            self.data['acc']['x'], self.data['acc']['y'], self.data['acc']['z'] = \
                                float(data_stream[0]), float(data_stream[1]), float(data_stream[2])

                            self.data['gyro']['x'], self.data['gyro']['y'], self.data['gyro']['z'] = \
                                float(data_stream[3]), float(data_stream[4]), float(data_stream[5])

                            self.data['magn']['x'], self.data['magn']['y'], self.data['magn']['z'] = \
                                float(data_stream[6]), float(data_stream[7]), float(data_stream[8])

                            # self.data['time'] = time.strftime("%Y-%m-%d %H:%M:%S")
                            time = datetime.datetime.now()
                            self.data['time'] = str(time.year)+"-"+str(time.month)+"-"+str(time.day)+" "+str(time.hour)+":"+str(time.minute)+":"+str(time.second)+"."+str(time.microsecond)
                            # print(self.data)
                            file = open(self.filename, "a+")
                            print(self.data)
                            # json.dump(self.data, file)

                            file.write(json.dumps(self.data, separators=(',', ': '), sort_keys=True)+"\n")
                            file.close()

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
                        time_str = time.strftime("%Y-%m-%d %H:%M:%S")
                        json_data = {'data': {}}
                        json_data['data'][time_str] = self.data
                        json_str = json.dumps(json_data)
                        with open(self.filename, "w") as json_file:
                            json_file.write (json_str)
        except serial.serialutil.SerialException as err:
            print(err)

    def get_recent_data(self):
        # Read the last line of the file efficiently
        return ast.literal_eval(self.get_last_line())

    def get_last_line(self):
        # https://stackoverflow.com/questions/7167008/efficiently-finding-the-last-line-in-a-text-file
        # file = open(self.filename, 'r')
        # file.seek(0, os.SEEK_END)  # seek to end of file; f.seek(0, 2) is legal
        # file.seek(file.tell() - 1, os.SEEK_SET)
        # data = file.read(1)
        # file.close()
        # print(data)
        # return data

        with open(self.filename, 'r') as f:
            lines = f.read().splitlines()
            last_line = lines[-1]
            return last_line

    def kill_threads(self):
        self.threads_ok = False
