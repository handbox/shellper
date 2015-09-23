import httplib2
import mock
import testtools

import shellper.base as base
import shellper.tests.unit.fake_class as base_test


class TestBase(testtools.TestCase):
    def setUp(self):
        super(TestBase, self).setUp()
        self.base_for_test = base.Base()
        self.config = {
            'time': '18:00',
            'date': '03.05',
            'summary': 'How clone git repository tomorrow?',
            'description': [['http://host1', 'http://host2']]
        }

    @mock.patch('argparse.ArgumentParser.parse_args', return_value={})
    def test_init_service(self, mock_argparse,):
        try:
            self.base_for_test._init_service()
        except httplib2.ServerNotFoundError:
            with testtools.ExpectedException(httplib2.ServerNotFoundError):
                self.base_for_test._init_service()

    @mock.patch('pygoogle.pygoogle')
    def test_search_query(self, mock_pygoogle):
        self.base_for_test.search_query([{"summary": "Test query"}])

    @mock.patch('oauth2client.file.Storage')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists', return_value=False)
    @mock.patch('shellper.base.Base._init_service',
                return_value={})
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value={})
    def test_authentication_exist(self, mock_argparse, mock_init_service,
                                  mock_exist, mock_mkdirs, mock_storage):
        self.base_for_test.authentication_in('gmail')

    @mock.patch('oauth2client.client.flow_from_clientsecrets')
    @mock.patch('oauth2client.tools.run_flow', return_value=None)
    @mock.patch('oauth2client.file.Storage')
    @mock.patch('os.makedirs')
    @mock.patch('os.path.exists', return_value=False)
    @mock.patch('shellper.base.Base._init_service',
                return_value={})
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=True)
    def test_authentication_not_exist(self, mock_argparse, mock_init_service,
                                      mock_exist, mock_mkdirs, mock_storage,
                                      mock_runflow, mock_client):
        base.CLIENT_SECRET_FILE = 'etc/client_secret1.json'
        self.base_for_test.authentication_in('gmail')

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    @mock.patch('googleapiclient.http.HttpRequest.execute', return_value={})
    def test_get_event_list_with_results(self, mock_init_service, mock_auth):
        self.base_for_test.get_event_list()

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass(out=True))
    @mock.patch('googleapiclient.http.HttpRequest.execute', return_value={})
    def test_get_event_list_without_results(self, mock_init_service,
                                            mock_service):
        self.base_for_test.get_event_list()

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    @mock.patch('shellper.base.Base._init_service', return_value={})
    @mock.patch('shellper.base.Base.authentication_in',
                return_value=base_test.FakeClass())
    @mock.patch('apiclient.discovery.build',
                return_value=base_test.FakeClass())
    @mock.patch('googleapiclient.http.HttpRequest.execute', return_value={
        'id': 'id'})
    def test_create_event(self, mock_execute, mock_build, mock_auth,
                          mock_service, mock__init_service):
        self.base_for_test.create_event(self.config)

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    def test_delete_event(self, mock_service):
        self.base_for_test.service = self.base_for_test._init_service()
        self.base_for_test.delete_event('some_id')

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    def test_quick_create(self, mock_init):
        self.base_for_test.service = self.base_for_test._init_service()
        self.base_for_test.quick_create_event(self.config)

    @mock.patch('shellper.base.Base.search_query', return_value=True)
    def test_add_links_with_results(self, mock_query):
        self.base_for_test.add_links(self.config)

    @mock.patch('shellper.base.Base.search_query', return_value=None)
    def test_add_links_without_results(self, mock_query):
        self.base_for_test.add_links(self.config)

    @mock.patch('shellper.base.Base._init_service',
                return_value=base_test.FakeClass())
    @mock.patch('shellper.base.Base.create_mail', return_value=None)
    def test_send_mail(self, mock_createmail, mock_init):
        self.base_for_test.send_mail(self.config, 'test@mail.com')

    @mock.patch('shellper.base.Base.add_links', return_value=None)
    def test_create_mail(self, mock_addlinks):
        self.base_for_test.create_mail(self.config, 'test@mail.com')
