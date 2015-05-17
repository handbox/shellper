import sys

import mock
import testtools

import shellper.base as base
import shellper.tests.base as base_test


class TestBase(testtools.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.base_for_test = base.Base()

    def test_search_query(self):
        self.base_for_test.search_query([{"summary": "Test query"}])

    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value={})
    def test_authentication(self, mock_argparse):
        del sys.argv[-1]
        self.base_for_test.authentication()

    @mock.patch('googleapiclient.http.HttpRequest.execute', returt_value=None)
    @mock.patch('shellper.base.Base.authentication',
                return_value=base_test.FakeClass())
    @mock.patch('apiclient.discovery.build',
                return_value=base_test.FakeClass())
    def test_get_event_list(self, mock_build, mock_auth, mock_googleapi):
        self.base_for_test.get_event_list()
