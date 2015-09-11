import sys

from shellper import main
from shellper.tests.integration import test_create_delete_event as clde
from shellper.tests.integration import test_create_send_mail as csm


def tests_scenarios():
    config = prepare_config()
    clde.TestCreateListDeleteEvent(config).scenario()
    csm.TestCreateSendMail(config).scenario()


def prepare_config():
        yaml_file = main.parsing_args()
        config = main.open_file(yaml_file)
        del sys.argv[-1]
        return config

if __name__ == "__main__":
    tests_scenarios()
