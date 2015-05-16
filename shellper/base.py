from pygoogle import pygoogle


class Base(object):

    def __init__(self):
        self.page_number = 1

    def search_query(self, query):
        request = pygoogle(query)
        request.pages = self.page_number
        return request.get_urls()
