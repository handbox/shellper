from shellper.tests.integration import abstract


class TestCreateListDeleteEvent(abstract.TestCase):
    def scenario(self):
        self.create_event(self.config)
        self.list_events()
        self.delete_event()
        self.ids_of_events = []
        self.quick_create(self.config)
        self.list_events()
        self.delete_event()

    def create_event(self, config):
        count = 0
        for event in config:
            self.ids_of_events.append(
                self.google.create_event(event))
            count += 1
        print 'Successfully created %s events!' % str(count)

    def list_events(self):
        print self.google.get_event_list()

    def delete_event(self):
        count = 0
        for id_of_event in self.ids_of_events:
            self.google.delete_event(id_of_event)
            count += 1
        print 'Successfully created %s events!' % str(count)

    def quick_create(self, config):
        count = 0
        for event in config:
            self.ids_of_events.append(
                self.google.quick_create_event(event))
            count += 1
        print 'Successfully created %s events!' % str(count)
