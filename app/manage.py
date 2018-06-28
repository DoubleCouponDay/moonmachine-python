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

def javascriptjobs():
    """using grunt because there will be multiple bundles in the future and separate node_modules files.
    """
    
    if DEBUG:         
        os.system("grunt development" + " --gruntfile ../grunt/grunt_webjob.js --verbose")

    else:
        os.system("grunt production" + " --gruntfile ../grunt/grunt_webjob.js --verbose")


def init():
    try: #clear the log
        with open(BASE_DIR + LOG_FILE, mode = 'w'):
            pass
            
    except Exception:
        pass

    try:
        if __name__ == "__main__":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

        execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "check"])
        execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "makemigrations"])
        execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "migrate", "--no-input"])
        execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "collectstatic", "--no-input", "--clear"])

        javascriptjobs()

        execute_from_command_line(sys.argv)

    except SystemExit:
        os._exit(1) #Ending a python script throws SystemExit exception. This line will allow me to debug gracefully.

init()
