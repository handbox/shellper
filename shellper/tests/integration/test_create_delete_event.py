import shellper.base as base
import shellper.main as run


class TestCreateListDeleteEvent(object):
    def __init__(self):
        config = [{
            'time': '22:00',
            'date': '18.05.2015',
            'summary': 'How clone git repository?'
        }]
        self.ids_of_events = []
        self.calendar = base.Base()
        self.create_event(config)
        self.list_events()
        self.delete_event()

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
