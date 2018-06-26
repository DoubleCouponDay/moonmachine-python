import os
from threading import Thread

class gruntwebjob(Thread):
    def __init__(self, entrypoint = str):
        super().__init__()
        self.__entrypoint = entrypoint
        self.start()

    def run(self):
        os.system("grunt --gruntfile ../grunt_webjob.js --verbose")    