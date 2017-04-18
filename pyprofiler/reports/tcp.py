import pyprofiler.reports
import pysniffer.l4.tcp

class OpenPortReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l4.tcp.OpenPortReport

    def handleReport(self, report, device):
        server = device['servers'].firstOrCreate(port=report.port, proto='tcp')
        server.incr('hits')

class ConnectsToReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l4.tcp.ConnectsToReport

    def handleReport(self, report, device):
        dst = report.dst
        for q in device['dns-queries']:
            if report.dst in q['response']:
                dst = q['query']
                break
        client = device['clients'].firstOrCreate(port=report.port, proto='tcp', dest=dst)
        client.incr('hits')