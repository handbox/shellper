class FakeClass(object):
    def __init__(self):
        self.argument = 'etc/template.yaml'

    def authorize(self, http):
        return None

    def build(self):
        return None
