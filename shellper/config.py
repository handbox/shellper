from oslo_config import cfg
from shellper import version


cli_opts = [
    cfg.StrOpt('remind_method', default='',
               help='Method for add you reminders.'),
    cfg.Opt('account', default='',
            help='If you choose set account for remind_method.')
]


CONF = cfg.CONF
CONF.register_cli_opts(cli_opts)


def parse_configs(conf_files=None):
    version_string = version.version_info.version_string()
    CONF(project='shellper', version=version_string,
         default_config_files=conf_files)
