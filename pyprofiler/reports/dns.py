import pyprofiler.reports
import pysniffer.l7.dns

class DnsQueryReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.dns.DnsQueryReport

    def handleReport(self, report, device):
        q = device['dns-queries'].firstOrCreate(query=report.query)
        q['response'] = list(set(report.response)) if not 'response' in q else list(set(q['response'] + report.response))
        