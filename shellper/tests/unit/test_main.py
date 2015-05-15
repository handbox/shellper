import mock
import testtools

import shellper.main as main_function


class FakeArgparse(object):
    def __init__(self):
        self.argument = 'etc/template.yaml'


class TestMain(testtools.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=FakeArgparse())
    @mock.patch('shellper.validation.validate')
    def test_main(self, mock_validate, mock_argparse):
        main_function.main()
