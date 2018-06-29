#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""
import os
import sys
from back.SelectionOptions.LabeledConstants import LOG_FILE
from django.core.management import execute_from_command_line
from settings import BASE_DIR, DEBUG
from threading import Thread
from javascriptjob import javascriptjob

def init():
    try: #clear the log
        with open(BASE_DIR + LOG_FILE, mode = 'w'):
            pass
            
    except Exception:
        pass

    try:
        if __name__ == "__main__":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

        execute_from_command_line(sys.argv)

    except SystemExit:
        os._exit(1) #Ending a python script throws SystemExit exception. This line will allow me to debug gracefully.

init()
