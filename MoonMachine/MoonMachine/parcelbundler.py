import os
from threading import Thread

class parcelbundler(Thread):
    def __init__(self, entrypoint = str):
        super().__init__()
        self.__entrypoint = entrypoint

    def run(self):
        os.system("parcel " + self.__entrypoint + " --out-dir ./static/dist")