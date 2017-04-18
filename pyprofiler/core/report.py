import pysniffer.l4.tcp
import pysniffer.l7.textmatch
import pyprofiler.core
import logging
import netaddr
logger = logging.getLogger(__name__)

class ReportHandler:
    @staticmethod
    def register(app):
        app.singleton(ReportHandler, ReportHandler, pyprofiler.core.InformationBase)

    def __init__(self, ib):
        self.ib = ib
        self.network = netaddr.IPNetwork('172.26.0.0/16')

        self.handlers = {}

    def boot(self):
        pass

    def registerHandler(self, report, handler):
        self.handlers[report] = handler
    
    def handleReport(self, report):
        if not report.host in self.network:
            return

        if not 'devices' in self.ib.root:
            self.ib.root['devices'] = []

        device = self.ib.root['devices'].first(host=report.host)
        
        
        #next((x for x in self.ib.root['devices'] if x['host'] == report.host), None)
        if device == None:
            device = {"host": report.host, "name": "Unknown Device", "servers": [], "clients": [], "dns-queries": []}
            self.ib.root['devices'].append(device)
            device = next((x for x in self.ib.root['devices'] if x['host'] == report.host), None)

        if report.__class__ in self.handlers:
            self.handlers[report.__class__](report, device)
        else:
            logger.error(f"Unhandled report: {type(report)}")

        return