import sys

import shellper.base as base
import shellper.main as run


class TestCreateListDeleteEvent(object):
    def __init__(self):
        self.ids_of_events = []
        self.calendar = base.Base()

    def scenario(self):
        self.create_event(self.prepare_config())
        self.list_events()
        self.delete_event()

    def prepare_config(self):
        yaml_file = run.parsing_args()
        config = run.open_file(yaml_file)
        del sys.argv[-1]
        return config

    def create_event(self, config):
        run.add_links(self.calendar, config)
        count = 0
        for event in config:
            self.ids_of_events.append(
                self.calendar.create_event(event))
            count += 1
        print 'Successfully created ' + str(count) + ' events!'

    def list_events(self):
        print self.calendar.get_event_list()

    def delete_event(self):
        count = 0
        for id_of_event in self.ids_of_events:
            self.calendar.delete_event(id_of_event)
            count += 1
        print 'Successfully deleted ' + str(count) + ' events!'
