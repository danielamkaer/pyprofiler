import pyprofiler.reports
import pysniffer.l4.udp
import netaddr

MULTICAST = netaddr.IPNetwork('224.0.0.0/4')
BROADCAST = netaddr.IPNetwork('255.255.255.255/32')

class OpenPortReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l4.udp.OpenPortReport

    def handleReport(self, report, device):
        server = device['servers'].firstOrCreate(port=report.port, proto='udp')
        server.incr('hits')

class ConnectsToReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l4.udp.ConnectsToReport

    def handleReport(self, report, device):
        if report.dst in MULTICAST or report.dst in BROADCAST:
            return

        dst = report.dst
        for q in device['dns-queries']:
            if report.dst in q['response']:
                dst = q['query']
                break
        client = device['clients'].firstOrCreate(port=report.port, proto='udp', dest=dst)
        client.incr('hits')