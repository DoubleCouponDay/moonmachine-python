from channels.generic.websocket import WebsocketConsumer
import json
from Back.Trading.RestGateways.ServerlessContext import ServerlessContext
from Back.Controllers.Pages import OUTPUT

serverlessContext = ServerlessContext()

class CompilationConsumer(WebsocketConsumer):
    """description of class"""
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, bytes_data):
        try:
            serverlessContext.SubmitScriptForCompilation(bytes_data, self)   
        
        except Exception as e:
            self.send(text_data = json.dumps({ 
                "output": str(e)
            }))

            