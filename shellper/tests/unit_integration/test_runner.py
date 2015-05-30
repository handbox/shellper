import mock
import testtools

from shellper.tests.integration import runner as runner


class TestRunner(testtools.TestCase):
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.__init__', return_value=None)
    @mock.patch('shellper.tests.integration.test_create_delete_event.'
                'TestCreateListDeleteEvent.scenario', return_value=None)
    def test_tests_scenarios(self, mock_init, mock_scenario):
        runner.tests_scenarios()
