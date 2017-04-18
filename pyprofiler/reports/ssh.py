import pyprofiler.reports
import pysniffer.l7.textmatch

class SshClientReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.textmatch.SshClientReport

    def handleReport(self, report, device):
        dst = report.dest
        for q in device['dns-queries']:
            if report.dest in q['response']:
                dst = q['query']
                break

        client = device['clients'].first(proto='tcp', port=report.port, dest=dst)
        client['service'] = 'ssh-client'
        
class SshServerReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.textmatch.SshServerReport

    def handleReport(self, report, device):
        server = device['servers'].first(proto='tcp', port=report.port)
        server['service'] = 'ssh-server'