import mock
import testtools

import shellper.main as main_function
import shellper.tests.base as base


class TestMain(testtools.TestCase):
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=base.FakeClass())
    @mock.patch('shellper.validation.validate')
    def test_main(self, mock_validate, mock_argparse):
        main_function.main()
