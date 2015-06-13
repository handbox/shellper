from shellper.tests.integration import test_create_delete_event as clde


def tests_scenarios():
    clde.TestCreateListDeleteEvent().scenario()

if __name__ == "__main__":
    tests_scenarios()
