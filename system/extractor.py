from interface import implements, Interface
import base64, requests
import httplib2


class IExtractor(Interface):

    def extract_news(self, url):
        pass


class Extractor(implements(IExtractor)):

    # return status code, indicating whether a successful connection can be made or not
    def check_url(self, url):
        decoded_url = base64.b64decode(url.encode()).decode()
        return requests.get(decoded_url).status_code

    # 202.45.139.16
    # http://202.45.139.16/readibility/vbtext.php?base64url=
    def extract_news(self, url):

        if (self.check_url(url) == 200):
            try:
                print('url', url)
                path = 'http://202.45.142.95/readibility/text.php?base64url=' + url
                print('path', path)
                # extracted_news = requests.get(path)

                http = httplib2.Http()
                content = http.request(path)[1]
                extracted_news = content.decode()
                print('extract', extracted_news)
                # extracted_news = 'malaysia aman dan damai'

                if extracted_news == "Looks like we couldn't find the content.":
                    return 'error extract'
                else:
                    return extracted_news

            except Exception as error:
                print('err', str(error))
                return 'error extract'

        else:
            return 'invalid URL'
