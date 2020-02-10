from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher


class NytimesLinkFetcher(DownloadLinkFetcher):
    ''' If you use http://spiderbites.nytimes.com/, you need to rewrite some methods.
        If you use nytimes api with key, it's the same with other corpus.
        This class uses the first website to crawl ntyime articles.
    
    '''

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')
        links = list()
        headlines_element = soup.find(id='headlines')
        elements = headlines_element.find_all('li')
        for element in elements:
            #print(str((element.a)['href']))
            links.append((element.a)['href'])

        return list(set(links))

