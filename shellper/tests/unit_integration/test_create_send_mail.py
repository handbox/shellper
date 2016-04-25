import mock
import testtools

from shellper.tests.integration import test_create_send_mail


class TestCreateSendMail(testtools.TestCase):
    def setUp(self):
        super(TestCreateSendMail, self).setUp()
        self.base = test_create_send_mail.TestCreateSendMail([{}])

    @mock.patch('shellper.base.Base.send_mail')
    def test_scenario(self, mock_sendmail):
        self.base.scenario()

    @mock.patch('shellper.base.Base.send_mail')
    def test_send_mail(self, mock_sendmail):
        self.base.test_send_mail()
