class LogHandler(logging.Handler):
    def emit(self, record):
        print("level=%(levelname)s \tname=%(name)s: %(message)s" % record.__dict__)
