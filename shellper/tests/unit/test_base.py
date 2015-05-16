import testtools

import shellper.base as base


class TestBase(testtools.TestCase):
    def test_search_query(self):
        base_for_test = base.Base()

        base_for_test.search_query([{"summary": "Test query"}])
