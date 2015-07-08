import sys

import shellper.base as base
import shellper.main as run


class TestCreateListDeleteEvent(object):
    def __init__(self):
        self.ids_of_events = []
        self.calendar = base.Base()

    def scenario(self):
        self.config = self.prepare_config()
        self.create_event(self.config)
        self.list_events()
        self.delete_event()
        self.ids_of_events = []
        self.quick_create(self.config)
        self.list_events()
        self.delete_event()

    def prepare_config(self):
        yaml_file = run.parsing_args()
        config = run.open_file(yaml_file)
        del sys.argv[-1]
        return config

    def create_event(self, config):
        count = 0
        for event in config:
            self.ids_of_events.append(
                self.calendar.create_event(event))
            count += 1
        print 'Successfully created %s events!' % str(count)

    def list_events(self):
        print self.calendar.get_event_list()

    def delete_event(self):
        count = 0
        for id_of_event in self.ids_of_events:
            self.calendar.delete_event(id_of_event)
            count += 1
        print 'Successfully created %s events!' % str(count)

    def quick_create(self, config):
        count = 0
        for event in config:
            self.ids_of_events.append(
                self.calendar.quick_create_event(event))
            count += 1
        print 'Successfully created %s events!' % str(count)
