import pyprofiler.core

class BaseReportHandler:
    def __init__(self, reportHandler):
        self.reportHandler = reportHandler

    @classmethod
    def register(cls, app):
        app.singleton(cls, cls, pyprofiler.core.ReportHandler)

    def boot(self):
        self.reportHandler.registerHandler(self.__class__.HANDLES, self.handleReport)