import jquery from "jquery";

export default function CompilationApi(subscriberFunc)
{
    return new Promise((resolve, reject) => {
        let self = this;
        self.baseUrl = 'ws://' + window.location.host + window.location.pathname + "ws/compilation"
        self.subscriberCallback = subscriberFunc;

        let publicStuff = {
            Subscribe: (subscriberFunc) => {
                self.subscriberCallback = subscriberFunc;
            },

            Send: (inputBytes) => {
                self.webSocket.send(inputBytes);
            },

            Dispose: () => {
                self.webSocket.close();
            }
        }

        self.webSocket = new WebSocket(self.baseUrl);

        self.webSocket.addEventListener('open', function () {
            publicStuff.Subscribe(subscriberFunc);
            resolve(publicStuff);
        });

        self.webSocket.addEventListener('message', function (event) {
            self.subscriberCallback(event);
        })
    });
}