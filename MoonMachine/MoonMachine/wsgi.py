"""
WSGI config for project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
from django.core.wsgi import get_wsgi_application
import sys
from django.core.management import execute_from_command_line
from dj_static import Cling

BASE_DIR = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(BASE_DIR, 'MoonMachine'))
sys.path.insert(0, BASE_DIR) #fixed bug where wsgi boot didnt have path configured correctly

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "check"])
execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "makemigrations"])
execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "migrate"])
execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "collectstatic", "--noinput"])


# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.

application = Cling(get_wsgi_application()) #cling adds static urls
