import os
import socket
import dj_database_url

class HiddenSettings(object):
    SECRET_KEY = 'f6881dd6-1e71-44e1-8059-f15ae29323e4'

    MY_HOSTNAME = 'DESKTOP-E62C0JN'

    FUNCTION_HOOK = 'https://mm-strategy-tasks-us.azurewebsites.net/api/'
    FUNCTION_HOST_KEY = 'xmB7WPOVXN0SESGUif6ypwI7NZZ00cazW8YKn/IIH9iJtnffvUFTGg=='

    POSTGRES_STRING = "postgres://kbueeqgsewyeqc:5974125120e3965a7e2b98ee19478523dbf1edcd951a3c2c796f20b4e6780c23@ec2-54-83-59-120.compute-1.amazonaws.com:5432/dcbt0gn4or00nq"

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