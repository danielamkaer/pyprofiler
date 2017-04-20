import pyprofiler.core
import pysniffer.core
import threading
import asyncio

import pysniffer.l4.tcp

def create_sniffer():
    return pysniffer.core.Application(ifname='br0s25')

class SnifferHandler:

    def __init__(self, sniffer, loop, ws, ib, reportHandler):
        self.sniffer = sniffer
        self.loop = loop
        self.ws = ws
        self.ib = ib
        self.sniffer.onReport += self.onReportBridge
        self.reportHandler = reportHandler

    def onReportBridge(self, *args):
        self.loop.call_soon_threadsafe(self.onReport, *args)
    
    def onReport(self, caller, report):
        self.reportHandler.handleReport(report)

    @staticmethod
    def register(app):
        app.singleton(pysniffer.core.Application, create_sniffer)
        app.singleton(SnifferHandler, SnifferHandler, pysniffer.core.Application, asyncio.BaseEventLoop, pyprofiler.core.WebSocketHandler, pyprofiler.core.InformationBase, pyprofiler.core.ReportHandler)
    
    def boot(self):
        self.thread = threading.Thread(target=self.sniffer.run)
        self.thread.start()

    def shutdown(self):
        self.sniffer.stop()
        self.thread.join()