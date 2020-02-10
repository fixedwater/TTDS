from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class ReutersLinkFetcher(DownloadLinkFetcher):

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        module_element = soup.find_all('div', class_='story-content')
        for classes in module_element:
            elements = classes.find_all('a')
            for element in elements:
                link = 'https://uk.reuters.com'+str(element['href'])
                #print(link)
                links.append(link)

        return list(set(links))
