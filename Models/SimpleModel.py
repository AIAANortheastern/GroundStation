import threading
import random


class SimpleModel:

    def __init__(self):
        self.data = 'Initialized. About to start Getting data'
        self.threads_ok = True
        t = threading.Thread(target=self._get_data)
        t.start()

    def _get_data(self):
        # This function should go ahead and pull data from the xbee.
        # we are going to need a loop that checks the serial port that the xbee is on for incoming data.
        # The current version here just has some dummy data

        # local data is a data structure intended to keep all of our data easily accessible when reading in random
        # packets form the radio.

        # it is structured like this:
        # - A list of different sensors
        #   - A dictionary with the code for that sensor as the key
        #       - A list of dictionaries with each output of the sensor.
        # so in this case we have the Altimeter -> alt with both of its paramaters, temperature -> temp and pressure ->
        # press
        # with the value of temp being 21.45 and the value of press being 500000
        while self.threads_ok:
            temp_val = random.randint(15, 30)
            press_val = random.randint(200000, 800000)
            local_data = [{'alt': [{'temp': temp_val}, {'press': press_val}]}]

            accel_x = random.random() * 3
            accel_y = random.random() * 3
            accel_z = random.random() * 3
            local_data.append({'accel': [{'x': accel_x}, {'y': accel_y}, {'z': accel_z}]})
            self.data = local_data

    def kill_threads(self):
        self.threads_ok = False

