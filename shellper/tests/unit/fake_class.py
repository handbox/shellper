class FakeClass(object):
    def __init__(self, out=False):
        self.argument = 'etc/template.yaml'
        self.out = out

    def authorize(self, http):
        return None

    def build(self):
        return None

    def events(self, **kwargs):
        return FakeClass(out=self.out)

    def list(self, **kwargs):
        return FakeClass(out=self.out)

    def execute(self):
        if self.out:
            return {}
        return {
            'items': [{
                'start': {
                    'dateTime': 'foo'
                },
                'summary': 'foo'
            }],
            'id': None}

    def insert(self, **kwargs):
        return FakeClass(out=self.out)

    def delete(self, **kwargs):
        return FakeClass(out=self.out)

    def quickAdd(self, **kwargs):
        return FakeClass(out=self.out)

    def users(self, **kwargs):
        return FakeClass(out=self.out)

    def messages(self, **kwargs):
        return FakeClass(out=self.out)

    def send(self, **kwargs):
        return FakeClass(out=self.out)
