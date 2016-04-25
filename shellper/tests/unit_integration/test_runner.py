import mock
import testtools

from shellper.tests.integration import runner


class TestRunner(testtools.TestCase):
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.scenario')
    @mock.patch('shellper.tests.integration.test_create_send_mail.'
                'TestCreateSendMail.scenario')
    @mock.patch('shellper.tests.integration.runner.prepare_config')
    def test_tests_scenarios(self, mock_csm, mock_cde, mock_prepare):
        runner.tests_scenarios()

    @mock.patch('shellper.main.parsing_args')
    @mock.patch('shellper.main.open_file')
    def test_prepare_config(self, mock_parsingargs, mock_open):
        runner.prepare_config()
