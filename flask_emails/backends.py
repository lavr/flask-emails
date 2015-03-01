# encoding: utf-8

class DummyResponse(object):
    status_code = 250

class DummyBackend(object):

    def __init__(self, **kw):
        pass

    def sendmail(self, **kw):
        return [DummyResponse()]