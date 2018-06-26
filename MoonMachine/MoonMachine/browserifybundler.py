import os
from threading import Thread

class browserifybundler(Thread):
    def __init__(self, entrypoint = str):
        super().__init__()
        self.__entrypoint = entrypoint

    def run(self):
        os.system("browserify " + self.__entrypoint + " --outfile " + self.__entrypoint)