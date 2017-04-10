import sys
import os
sys.path.append(os.path.realpath('../pysniffer'))

import pyprofiler.core

app = pyprofiler.core.Application(sys.argv)
app.register(pyprofiler.core.WebApplication)
app.register(pyprofiler.core.WebSocketHandler)
app.register(pyprofiler.core.InformationBase)
app.register(pyprofiler.core.SnifferHandler)
app.run()
