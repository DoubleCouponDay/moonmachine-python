import os
import socket
import dj_database_url

class HiddenSettings(object):
    SECRET_KEY = 'ba044add-de9b-418f-9a71-5d40ff151124'

    MY_HOSTNAME = 'DESKTOP-E62C0JN'

    FUNCTION_HOOK = 'https://mm-strategy0tasks.azurewebsites.net/api/'
    FUNCTION_HOST_KEY = 'nJLJYZrF1foWJS1/v8jxYy5Rk1mv5MT5yTrbLNZJVNdffNt8Jglwsg=='

    POSTGRES_STRING = "postgres://qjsdqutoeltlwg:7e17d9ca493e3080ada1391fc06b700f5ee38a41ae8e39e27f4dd66d07846583@ec2-54-83-59-120.compute-1.amazonaws.com:5432/dcbt0gn4or00nq"

    def __init__(self):
        self.currentHost = socket.gethostname()

    def GetFunctionHook(self):
        if self.currentHost != HiddenSettings.MY_HOSTNAME:
            return HiddenSettings.FUNCTION_HOOK

        else:
            return "http://localhost:7071/api/"

    def GetFunctionHostKey(self):
        if self.currentHost != HiddenSettings.MY_HOSTNAME:
            return HiddenSettings.FUNCTION_HOST_KEY

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