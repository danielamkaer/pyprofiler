import pyprofiler.reports
import pysniffer.l7.textmatch

class HttpClientReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.textmatch.HttpClientReport

    def handleReport(self, report, device):
        dst = report.dest
        for q in device['dns-queries']:
            if report.dest in q['response']:
                dst = q['query']
                break

        client = device['clients'].first(proto='tcp', port=report.port, dest=dst)
        client['service'] = 'http-client'
        
class HttpServerReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.textmatch.HttpServerReport

    def handleReport(self, report, device):
        server = device['servers'].first(proto='tcp', port=report.port)
        server['service'] = 'http-server'