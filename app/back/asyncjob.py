from threading import Thread

class asyncjobber(Thread):
    def __init__(self, jobfunction):
        super().__init__()
        self.__jobfunction = jobfunction
        self.start()

    def run(self):
        self.__jobfunction()