import mock
from oslo_config import cfg
import testtools

import shellper.main as main_function
import shellper.tests.unit.fake_class as base


class TestMain(testtools.TestCase):

    @mock.patch('shellper.base.Base.send_mail', return_value=None)
    @mock.patch('shellper.base.Base.add_links', retur_value=None)
    @mock.patch('shellper.base.Base.create_event', return_value=None)
    @mock.patch('shellper.base.Base.search_query', return_value=None)
    @mock.patch('shellper.base.Base.get_event_list', return_value=[])
    @mock.patch('argparse.ArgumentParser.parse_args',
                return_value=base.FakeClass())
    @mock.patch('shellper.validation.validate')
    def test_main_without_events(self, mock_validate, mock_argparse,
                                 mock_getlist, mock_query, mock_create,
                                 mock_links, mock_mail):
        conf = cfg.CONF.remind_method
        cfg.CONF.remind_method = 'mail'
        main_function.main()
        cfg.CONF.remind_method = 'calendar'
        main_function.main()
        cfg.CONF.remind_method = ''
        main_function.main()
        cfg.CONF.remind_method = conf
