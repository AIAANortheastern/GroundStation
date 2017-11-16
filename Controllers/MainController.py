from Models.SimpleModel import SimpleModel
from Views.TextView import TextView


class MainController:

    def __init__(self):
        self.model = SimpleModel()
        self.view = TextView()

    def run(self):
        self.view.display(self.model)

