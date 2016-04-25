from shellper import base


class TestCase(object):
    def __init__(self, config):
        self.ids_of_events = []
        self.config = config
        self.google = base.Base()
