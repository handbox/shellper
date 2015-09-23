import mock
import testtools

from shellper import config


class TestConfig(testtools.TestCase):
    @mock.patch('oslo_config.cfg.ConfigOpts.__call__')
    def test_parse_configs(self, mock_configopts):
        config.parse_configs()
