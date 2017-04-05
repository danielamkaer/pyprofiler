import pyprofiler.core
from aiohttp import web

class Client:
    def __init__(self, ws):
        self.ws = ws

class WebSocketHandler:
    def __init__(self, app):
        self.app = app
        self.clients = []

    @staticmethod
    def register(app):
        app.singleton(WebSocketHandler, WebSocketHandler, web.Application)

    def boot(self):
        print("WebSocketHandler booted")
        self.app.router.add_get('/ws', self.websocket_handler)

    def emit_all(self, msg):
        for cli in self.clients:
            cli.ws.send_json(msg)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        cli = Client(ws)
        self.clients.append(cli)
        print("socket opened")
        ib = self.container[pyprofiler.core.InformationBase]
        ws.send_json(['ib',{'update':'UPDATE_SET','path':'','item':ib.root}])
        async for msg in ws:
            print(msg)
        print("socket closed")
        self.clients.remove(cli)

        return ws