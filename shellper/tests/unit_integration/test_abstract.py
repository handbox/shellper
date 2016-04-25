import testtools

from shellper.tests.integration import abstract


class TestAbstaract(testtools.TestCase):
    def test_init(self):
        abstract.TestCase({})
