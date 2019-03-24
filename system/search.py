from interface import implements, Interface
from googleapiclient.discovery import build


class ISearching(Interface):

    def search_news(self, keyword):
        pass



class Searching(implements(ISearching)):

    def search_news(self, keyword):

        # build custom search service
        service = build(serviceName="customsearch", version="v1", developerKey="")

        # get response based on the keyword passed to the service
        response = service.cse().list(q=keyword, cx='').execute()

        return response['items']
