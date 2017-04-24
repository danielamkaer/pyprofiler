import pyprofiler.reports
import pysniffer.l7.dhcp

class DhcpReportHandler(pyprofiler.reports.BaseReportHandler):
    HANDLES = pysniffer.l7.dhcp.DhcpReport

    def handleReport(self, report, device):
        if report.hostname:
            device['name'] = report.hostname
         