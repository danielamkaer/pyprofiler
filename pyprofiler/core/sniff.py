import pyprofiler.core
import pysniffer.core
import threading
import asyncio

import pysniffer.l4.tcp

def create_sniffer():
    return pysniffer.core.Application(['','br0s25'])

class SnifferHandler:

    def __init__(self, sniffer, loop, ws, ib):
        self.sniffer = sniffer
        self.loop = loop
        self.ws = ws
        self.ib = ib
        self.sniffer.onReport += self.onReportBridge

    def onReportBridge(self, *args):
        self.loop.call_soon_threadsafe(self.onReport, *args)
    
    def onReport(self, caller, report):
        if isinstance(report, pysniffer.l4.tcp.OpenPortReport):
            #self.ws.emit_all(['report', report.__dict__])
            if not 'devices' in self.ib.root:
                self.ib.root['devices'] = []
            
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            if not dev:
                dev = {'name': report.host, 'ports':[report.port]}
                self.ib.root['devices'].append(dev)
            else:
                if report.port not in dev['ports']:
                    dev['ports'].append(report.port)

    @staticmethod
    def register(app):
        app.singleton(pysniffer.core.Application, create_sniffer)
        app.singleton(SnifferHandler, SnifferHandler, pysniffer.core.Application, asyncio.BaseEventLoop, pyprofiler.core.WebSocketHandler, pyprofiler.core.InformationBase)
    
    def boot(self):
        self.thread = threading.Thread(target=self.sniffer.run)
        self.thread.start()