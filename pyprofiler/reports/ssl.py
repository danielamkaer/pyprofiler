import pyprofiler.reports
import pysniffer.l7.ssl

class SslClientReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.ssl.SslClientReport

    def handleReport(self, report, device):
        dst = report.dest
        for q in device['dns-queries']:
            if report.dest in q['response']:
                dst = q['query']
                break
        report = device['clients'].first(proto='tcp', port=report.port, dest=dst)
        if report:
            report['service'] = 'ssl-client'