import os
import sys

import argparse
import yaml
from oslo_config import cfg

import shellper.base as base
from shellper import config
import shellper.validation as validation


# Parsing of arguments from tox
def parsing_args():
    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument('argument', help="Path to template file",
                        nargs='?')
    args = parser.parse_args()
    return args.argument


# Open yaml file and conver to json
def open_file(argument):
    with open(argument, 'r') as yaml_file:
        return yaml.load(yaml_file)


def setup_common():
    dev_conf = os.path.join('etc',
                            'shellper',
                            'shellper.conf')
    config_files = None
    if os.path.exists(dev_conf):
        config_files = [dev_conf]

    config.parse_configs(config_files)


def main():
    argument = parsing_args()
    request = open_file(argument)
    validation.validate(request)
    del sys.argv[-1]
    setup_common()

    google = base.Base()

    remind_method = cfg.CONF.remind_method
    to = cfg.CONF.account
    if remind_method == 'mail':
        for event in request:
            google.send_mail(event, to)
    elif remind_method == 'calendar':
        for event in request:
            google.create_event(event)
    elif not remind_method:
        for event in request:
            google.create_event(event)
            google.send_mail(event, to)

if __name__ == "__main__":
    main()
