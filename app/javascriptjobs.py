from os import system, chdir
from threading import Thread
from logging import Logger, getLogger

class javascriptjobs:
    def __init__(self, debugmode = bool, entrypoint = str):
        self.__log = getLogger(str(self.__class__))
        self.__debugmode = debugmode
        self.__entrypoint = entrypoint
        self.__log.info("running javascript tasks in series.")
        self.__runtasks()

    def __runtasks(self):
        """using grunt because there will be multiple bundles in the future"""
        
        if self.__debugmode:            
            system("grunt development" + " --gruntfile ../grunt_webjob.js --verbose")

        else:
            system("grunt production" + " --gruntfile ../grunt_webjob.js --verbose")