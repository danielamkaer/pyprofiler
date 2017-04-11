import pysniffer.l4.tcp
import pysniffer.l7.textmatch
import pyprofiler.core
import logging
logger = logging.getLogger(__name__)

class ReportHandler:
    @staticmethod
    def register(app):
        app.singleton(ReportHandler, ReportHandler, pyprofiler.core.InformationBase)

    def __init__(self, ib):
        self.ib = ib

    def boot(self):
        pass

    def handleReport(self, report):
        if isinstance(report, pysniffer.l4.tcp.OpenPortReport):
            #self.ws.emit_all(['report', report.__dict__])
            if not 'devices' in self.ib.root:
                self.ib.root['devices'] = []
            
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            if not dev:
                dev = {'name': report.host, 'ports':[report.port], 'services': [], 'clients': []}
                self.ib.root['devices'].append(dev)
            else:
                if report.port not in dev['ports']:
                    dev['ports'].append(report.port)

        elif isinstance(report, pysniffer.l4.tcp.ConnectsToReport):
            #self.ws.emit_all(['report', report.__dict__])
            if not 'devices' in self.ib.root:
                self.ib.root['devices'] = []
            
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            if not dev:
                dev = {'name': report.host, 'ports':[], 'services': [], 'clients': []}
                self.ib.root['devices'].append(dev)
        
        elif isinstance(report, pysniffer.l4.udp.OpenPortReport):
            if not 'devices' in self.ib.root:
                self.ib.root['devices'] = []

            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            if not dev:
                dev = {'name': report.host, 'ports':[report.port], 'services': [], 'clients' :[]}
                self.ib.root['devices'].append(dev)
            else:
                if report.port not in dev['ports']:
                    dev['ports'].append(report.port)
        
        elif isinstance(report, pysniffer.l4.udp.ConnectsToReport):
            if not 'devices' in self.ib.root:
                self.ib.root['devices'] = []
            
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            if not dev:
                dev = {'name': report.host, 'ports':[], 'services': [], 'clients': []}
                self.ib.root['devices'].append(dev)

        elif isinstance(report, pysniffer.l7.textmatch.SshServerReport):
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            dev['services'].append({'service':'ssh-server', 'port':report.port})

        elif isinstance(report, pysniffer.l7.textmatch.HttpServerReport):
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            dev['services'].append({'service':'http-server', 'port':report.port})

        elif isinstance(report, pysniffer.l7.textmatch.HttpClientReport):
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            dev['clients'].append({'client':'http-client', 'remote': report.dest, 'port':report.port})

        elif isinstance(report, pysniffer.l7.textmatch.SshClientReport):
            dev = next((x for x in self.ib.root['devices'] if x['name'] == report.host), None)
            dev['clients'].append({'client':'ssh-client', 'remote': report.dest, 'port':report.port})

        else:
            logger.error(f"Unhandled report: {type(report)}")