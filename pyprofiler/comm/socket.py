import pyprofiler.core


class SocketManager:
    def __init__(self):
        self.protocols = {}

    def addProtocol(self, name, proto):
        self.protocols[name] = proto

    def prepareSocket(self, ws):
        sock = Socket(ws)

        for key in self.protocols:
            sock.registerProtocol(key, self.protocols[key])

        return sock


class Socket:
    def __init__(self, ws):
        self.ws = ws
        self.protocols = {}

    def onMessage(self, msg):
        pass

    def sendmessage(self, proto, data):
        self.ws.send_json([proto, data])

    def registerProtocol(self, name, proto):
        self.protocols[name] = proto


class Protocol:
    def __init__(self, sock, name):
        self.socket = sock
        self.name = name

        self.onMessage = pysniffer.core.Event()

    def handleMessage(self, message):
        self.onMessage(message)

    def sendMessage(self, data):
        self.socket.sendMessage(self.name, data)
