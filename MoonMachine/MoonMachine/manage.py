#!/usr/bin/env python
"""
Command-line utility for administrative tasks.
"""
import os
import sys
from settings import BASE_DIR
from back.SelectionOptions.LabeledConstants import LOG_FILE
from django.core.management import execute_from_command_line

try: #in case filedoes not exist
    with open(BASE_DIR + LOG_FILE, mode = 'w') as clearedLog:
        pass
except Exception:
    pass

try:
    if __name__ == "__main__":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "check"])
    execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "makemigrations"])
    execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "migrate"])
    execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "collectstatic", "--no-input"])
    execute_from_command_line(sys.argv)

except SystemExit:
    os._exit(1); #Ending a python script throws SystemExit exception. This line will allow me to debug gracefully.
