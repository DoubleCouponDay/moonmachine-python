import os
import socket
import dj_database_url

class HiddenSettings(object):
    SECRET_KEY = 'f6881dd6-1e71-44e1-8059-f15ae29323e4'

    MY_HOSTNAME = 'DESKTOP-E62C0JN'

    FUNCTION_HOOK = 'https://mm-strategy-tasks-us.azurewebsites.net/api/'
    FUNCTION_HOST_KEY = 'xmB7WPOVXN0SESGUif6ypwI7NZZ00cazW8YKn/IIH9iJtnffvUFTGg=='

    POSTGRES_STRING = "postgres://yygogszhxnbzmn:efce0e974c883492064e70b0ef16ce15f8f3e6eab294c055b5b9eb12e860ff01@ec2-23-23-130-158.compute-1.amazonaws.com:5432/dbhl079gfuhqn4"

    def __init__(self):
        self.currentHost = socket.gethostname()

    def GetFunctionHook(self):
        if self.currentHost != HiddenSettings.MY_HOSTNAME:
            return FUNCTION_HOOK

        else:
            return "http://localhost:7071/api/"

    def GetFunctionHostKey(self):
        if self.currentHost != HiddenSettings.MY_HOSTNAME:
            return FUNCTION_HOST_KEY

        else:
            return ""

    def GetDebugFlag(self):
        try:
            possibleDebugMode = os.environ["DEBUG_MODE"] #tightly couple to heroku cong vars. I dont care.
            return False

        except:
            return True

    def GetDatabaseConfig(self):
        output = {}
        currentHostname = socket.gethostname()

        if currentHostname != HiddenSettings.MY_HOSTNAME:
            #empty host argument means localhost
            output['default'] = dj_database_url.config(default=HiddenSettings.POSTGRES_STRING)

        else:
            output['default'] = {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'postgres',
                'HOST': '', 
                'PORT': '5432',
                'AUTOCOMMIT': True,
                'USER': 'postgres',
                'PASSWORD': 'postgres'
            }
        return output