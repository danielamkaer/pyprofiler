import pyprofiler.core
from aiohttp import web
import json

class Client:
    def __init__(self, ws):
        self.ws = ws

class WebSocketHandler:
    def __init__(self, app, ib):
        self.app = app
        self.clients = []
        self.ib = ib

        self.ib.onInformationChanged += self.onInformationChanged

    async def onInformationChanged(self, info):
        self.emit_all(['ib', info])

    @staticmethod
    def register(app):
        app.singleton(WebSocketHandler, WebSocketHandler, web.Application, pyprofiler.core.InformationBase)

    def boot(self):
        print("WebSocketHandler booted")
        self.app.router.add_get('/ws', self.websocket_handler)

    async def shutdown(self):
        for cli in self.clients:
            await cli.ws.close()

    def emit_all(self, msg):
        for cli in self.clients:
            cli.ws.send_json(msg)

    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        cli = Client(ws)
        self.clients.append(cli)
        print("socket opened")
        ws.send_json(['ib',{'update':'UPDATE_SET','path':'','item':self.ib.root}])
        async for msg in ws:
            print(msg)
        print("socket closed")
        self.clients.remove(cli)

        return ws