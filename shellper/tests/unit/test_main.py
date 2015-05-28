import mock
import testtools

import shellper.base as main_base
import shellper.main as main


class TestMain(testtools.TestCase):
    @mock.patch('shellper.main.open_file')
    @mock.patch('shellper.main.parsing_args')
    @mock.patch('shellper.base.Base.create_event', return_value=None)
    @mock.patch('shellper.base.Base.search_query', return_value=None)
    @mock.patch('shellper.base.Base.get_event_list', return_value=None)
    @mock.patch('shellper.validation.validate')
    def test_main(self, mock_validate, mock_getlist, mock_query, mock_create,
                  mock_argparse, mock_openfile):
        main.main()

    @mock.patch('argparse.ArgumentParser.parse_args')
    def test_parsing_args(self, mock_argparse):
        main.parsing_args()

    def test_open_file(self):
        main.open_file('etc/template.yaml')

    @mock.patch('shellper.base.Base.search_query', return_value=None)
    def test_add_links(self, mock_query):
        config = [{
            'time': '22:00',
            'date': '18.05.2015',
            'summary': 'How clone git repository?'
        }]
        main.add_links(main_base.Base(), config)
