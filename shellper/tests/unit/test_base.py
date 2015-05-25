import mock
import testtools

import shellper.base as base
import shellper.tests.base as base_test


class TestBase(testtools.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.base_for_test = base.Base()

    @mock.patch('pygoogle.pygoogle')
    def test_search_query(self, mock_pygoogle):
        self.base_for_test.search_query([{"summary": "Test query"}])

    @mock.patch('shellper.base.Base._init_service',
                return_value={})
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value={})
    def test_authentication(self, mock_argparse, mock_init_service):
        self.base_for_test.authentication()

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    @mock.patch('shellper.base.Base.authentication',
                return_value=base_test.FakeClass())
    @mock.patch('googleapiclient.http.HttpRequest.execute', return_value={})
    @mock.patch('apiclient.discovery.build',
                return_value=base_test.FakeClass())
    def test_get_event_list(self, mock_init_service, mock_googleapi,
                            mock_auth, mock_service):
        self.base_for_test.get_event_list()

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    @mock.patch('shellper.base.Base._init_service', return_value={})
    @mock.patch('shellper.base.Base.authentication',
                return_value=base_test.FakeClass())
    @mock.patch('apiclient.discovery.build',
                return_value=base_test.FakeClass())
    @mock.patch('googleapiclient.http.HttpRequest.execute', return_value={
        'id': 'id'})
    def test_create_event(self, mock_execute, mock_build, mock_auth,
                          mock_service, mock__init_service):
        self.base_for_test.service = self.base_for_test._init_service()
        json = {
            'time': '18:00',
            'date': '03.05',
            'summary': 'How clone git repository?',
            'description': 'http://host1 http://host2'
        }
        self.base_for_test.create_event(json)
