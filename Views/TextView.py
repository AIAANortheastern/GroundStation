import time


class TextView:

    def __init__(self):
        pass

    def display(self, model):
        while True:
            # get the key and the value from each entry in the dictionary
            data = ''
            for key, value in model.data.items():
                data += '{0}:'.format(key)
                for results_key, results_value in value.items():
                    data += ' {0}: {1}'.format(results_key, results_value)
                data += '\t\t'
            time_stamp = time.strftime("%Y,%m,%d,%H:%M:%S")
            print("{0}: {1}".format(time_stamp, data))
            time.sleep(1)

