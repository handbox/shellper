from shellper.tests.integration import test_create_delete_event as basic


def tests_scenarios():
    basic.TestCreateListDeleteEvent().scenario()

if __name__ == "__main__":
    tests_scenarios()
