from interface import implements, Interface
import base64, requests


class IExtractor(Interface):

    def extract_news(self, url):
        pass



class Extractor(implements(IExtractor)):

    # return status code, indicating whether a successful connection can be made or not
    def check_url(self, url):
        decoded_url = base64.b64decode(url.encode()).decode()
        return requests.get(decoded_url).status_code

#202.45.139.16
    def extract_news(self, url):

        if(self.check_url(url) == 200):
            try:
                extracted_news = requests.get('http://202.45.139.16/readibility/vbtext.php?base64url=' + url).text
                if extracted_news == "Looks like we couldn't find the content.":
                    return 'error extract'
                else:
                    return extracted_news

            except:
                return 'error extract'

        else:
            return 'invalid URL'