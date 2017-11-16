import time


class TextView:

    def __init__(self):
        pass

    def display(self, model):
        while True:
            # get the key and the value from each entry in the dictionary
            data = ''
            for sensor in model.data:
                for key, value in sensor.items():
                    data += '{0}:'.format(key)
                    for item in value:
                        for results_key, results_value in item.items():
                            data += ' {0}: {1}'.format(results_key, results_value)
                data += '\t\t'
            print(data)
            time.sleep(1)

