from channels.generic.websocket import WebsocketConsumer
import json
from back.RestGateways.ServerlessContext import ServerlessContext
from back.Controllers.Pages import OUTPUT

serverlessContext = ServerlessContext()

class CompilationConsumer(WebsocketConsumer):
    """description of class"""
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, bytes_data): #fixed bug where channel's websocketbridge used text data instead of bytes_data
        try:
            serverlessContext.SubmitScriptForCompilation(bytes_data, self)   
        
        except Exception as e:
            self.send(text_data = json.dumps({ 
                "unknown error: ": str(e)
            }))

            