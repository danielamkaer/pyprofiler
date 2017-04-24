import sys
import os
sys.path.append(os.path.realpath('../pysniffer'))

import pyprofiler.core
import pyprofiler.reports.tcp
import pyprofiler.reports.udp
import pyprofiler.reports.dns
import pyprofiler.reports.http
import pyprofiler.reports.ssh
import pyprofiler.reports.ssl
import pyprofiler.reports.dhcp

app = pyprofiler.core.Application(sys.argv)
app.register(pyprofiler.core.WebApplication)
app.register(pyprofiler.core.WebSocketHandler)
app.register(pyprofiler.core.InformationBase)
app.register(pyprofiler.core.SnifferHandler)
app.register(pyprofiler.core.ReportHandler)
app.register(pyprofiler.reports.tcp.OpenPortReportHandler)
app.register(pyprofiler.reports.tcp.ConnectsToReportHandler)
app.register(pyprofiler.reports.udp.OpenPortReportHandler)
app.register(pyprofiler.reports.udp.ConnectsToReportHandler)
app.register(pyprofiler.reports.dns.DnsQueryReportHandler)
app.register(pyprofiler.reports.http.HttpClientReportHandler)
app.register(pyprofiler.reports.http.HttpServerReportHandler)
app.register(pyprofiler.reports.ssh.SshClientReportHandler)
app.register(pyprofiler.reports.ssh.SshServerReportHandler)
app.register(pyprofiler.reports.ssl.SslClientReportHandler)
app.register(pyprofiler.reports.dhcp.DhcpReportHandler)
app.run()
