import mock
import testtools

import shellper.tests.integration.test_create_delete_event as test_integration


class TestCreateDeleteEvent(testtools.TestCase):
    def setUp(self):
        super(TestCreateDeleteEvent, self).setUp()
        self.test_cld = test_integration.TestCreateListDeleteEvent()

    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.delete_event')
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.list_events')
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.create_event')
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.prepare_config')
    def test_scenario(self, mock_prepare, mock_create, mock_list, mock_delete):
        self.test_cld.scenario()

    @mock.patch('shellper.main.open_file')
    @mock.patch('shellper.main.parsing_args')
    def test_prepare_config(self, mock_args, mock_open):
        self.test_cld.prepare_config()

    @mock.patch('shellper.base.Base.create_event')
    @mock.patch('shellper.main.add_links')
    def test_create_event(self, mock_links, mock_create_event):
        config = {
            'time': '18:00',
            'date': '03.05',
            'summary': 'How clone git repository?'
        }
        test_integration.TestCreateListDeleteEvent().create_event(config)

    @mock.patch('shellper.base.Base.get_event_list')
    def test_list_events(self, mock_get_event_list):
        self.test_cld.list_events()

    @mock.patch('shellper.base.Base.delete_event')
    def test_delete_event(self, mock_delete_event):
        self.test_cld.ids_of_events = [1, 2, 3]
        self.test_cld.delete_event()
