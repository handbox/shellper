class FakeClass(object):
    def __init__(self):
        self.argument = 'etc/template.yaml'

    def authorize(self, http):
        return None

    def build(self):
        return None

    def events(self):
        return FakeClass()

    def list(self, **kwargs):
        return FakeClass()

    def execute(self):
        return {'items': [], 'id': None}

    def insert(self, **kwargs):
        return FakeClass()
