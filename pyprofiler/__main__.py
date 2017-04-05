import sys
sys.path.append('/home/daniel/pysniffer')

import pyprofiler.core

app = pyprofiler.core.Application(sys.argv)
app.register(pyprofiler.core.WebApplication)
app.register(pyprofiler.core.WebSocketHandler)
app.register(pyprofiler.core.InformationBase)
app.register(pyprofiler.core.SnifferHandler)
app.run()
