from interface import implements, Interface
import requests
from bs4 import BeautifulSoup


class ISpecialExtractor(Interface):

    def special_scraping(self, link):
        pass


class SpecialExtractor(implements(ISpecialExtractor)):

    def special_scraping(self, link):
        page = requests.get(link)
        html = page.content.decode()
        soup = BeautifulSoup(page.content, 'html.parser')

        title, article_lead, article_body, source, date = '', '', '', '', ''

        if 'utusan.com.my' in link:
            title, article_lead, article_body, source, date = self.scrape_utusan(soup)
        elif 'bharian.com.my' in link:
            title, article_lead, article_body, source, date = self.scrape_bharian(soup)
        elif 'astroawani.com' in link:
            title, article_lead, article_body, source, date = self.scrape_awani(soup)
        elif 'hmetro.com.my' in link:
            title, article_lead, article_body, source, date = self.scrape_hmetro(soup)
        elif 'kosmo.com.my' in link:
            title, article_lead, article_body, source, date = self.scrape_kosmo(soup)
        elif 'mstar.com.my' in link:
            title, article_lead, article_body, source, date = self.scrape_mstar(soup)

        return html, title, article_lead, article_body, source, date

    def scrape_utusan(self, soup):
        title = soup.find("h1", {"class":"articleTitle content__headline js-score"}).get_text()
        date = soup.find("time", {"class":"content__dateline-wpd js-wpd content__dateline-wpd--modified"}).get_text()
        article_lead = soup.find("p", class_="lead").get_text()
        article_body = soup.select('div.articleBody p')
        source = "Utusan Malaysia"

        article_body2 = article_lead + ' '
        for data in article_body:
            article_body2 += data.get_text() + ' '

        article_body2 = article_body2.replace(' - UTUSAN ONLINE', '')
        article_body2 = article_body2.replace('-UTUSAN ONLINE', '')
        article_body2 = article_body2.replace('- UTUSAN ONLINE', '')
        article_body2 = article_body2.replace(' -UTUSAN ONLINE', '')

        return title.strip(), article_lead.strip(), article_body2.strip(), source, date.strip()

    def scrape_bharian(self, soup):
        title = soup.select("h1.page-header")
        print(title)
        date = soup.find("div", "node-meta")
        #print(date)
        article_body = soup.select("div.field-items div.field-item even p")
        #print(article_body)
        article_lead = ''
        source = "Berita Harian"

        article_body2 = ''
        for data in article_body:
            article_body2 += data.get_text() + ' '

        return title, article_lead, article_body2, source, date


    def scrape_awani(self, soup):
        title = soup.find("h1", class_="col-xs-12").get_text()
        date = soup.find("span", class_="author-text").contents[-1].strip()
        article_body = soup.select("div.detail-body-content")
        article_lead = article_body[0].get_text().split('.')[0] + ' ' + article_body[0].get_text().split('.')[1]
        source = "Astro Awani"

        article_body2 = ''
        for data in article_body:
            article_body2 += data.get_text() + ' '

        return title.strip(), article_lead.strip(), article_body2.strip(), source, date.strip()


    def scrape_hmetro(self, soup):
        title = soup.find("h1", class_="page-header").get_text()
        date = soup.find(class_="published-date").get_text()
        article_body = soup.select("div.field-item p")
        article_lead = article_body[1].get_text() + ' ' + article_body[2].get_text()
        source = "Harian Metro"

        article_body2 = ''
        for data in article_body:
            article_body2 += data.get_text() + ' '

        date = date.replace('Artikel ini disiarkan pada :', '')

        return title.strip(), article_lead.strip(), article_body2.strip(), source, date.strip()


    def scrape_kosmo(self, soup):
        title = soup.find("h1", class_="article-title_title").get_text()
        date = soup.find("span", class_="date").get_text()
        article_lead = soup.find("p", class_="lead").get_text()
        article_body = soup.select('div.articleBody p')
        source = "Kosmo!"

        article_body2 = article_lead + ' '
        for data in article_body:
            article_body2 += data.get_text() + ' '

        article_body2 = article_body2.replace(' - Bernama', '')
        article_body2 = article_body2.replace(' - K! ONLINE', '')

        return title.strip(), article_lead.strip(), article_body2.strip(), source, date.strip()


    def scrape_mstar(self, soup):
        title = soup.find("h1", class_="fl").get_text()
        date = soup.find("label", class_="byline").get_text()
        article_body = soup.select("article.story p")
        article_lead = article_body[0].get_text() + ' ' + article_body[1].get_text()
        source = "mStar"

        article_body2 = ''
        for data in article_body:
            article_body2 += data.get_text() + ' '

        article_lead = article_lead.replace('DIKEMASKINI', '')
        article_body2 = article_body2.replace('DIKEMASKINI', '')
        article_body2 = article_body2.replace(' - The Star', '')
        article_body2 = article_body2.replace(' - Bernama', '')

        return title.strip(), article_lead.strip(), article_body2.strip(), source, date.strip()



specialobject = SpecialExtractor()
html, title, article_lead, article_body, source, date = specialobject.special_scraping('https://www.bharian.com.my/dunia/amerika/2019/01/519188/remaja-arab-saudi-tiba-di-kanada')

print(title)
print(article_lead)
print(article_body)
print(source)
print(date)