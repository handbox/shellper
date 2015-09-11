from shellper.tests.integration import abstract


class TestCreateSendMail(abstract.TestCase):
    def scenario(self):
        self.test_send_mail()

    def test_send_mail(self):
        for event in self.config:
            self.google.send_mail(event, 'handbox.inc@gmail.com')
