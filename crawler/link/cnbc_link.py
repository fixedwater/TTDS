from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class CnbcLinkFetcher(DownloadLinkFetcher):


    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        # news links are the hrefs of a
        elements = soup.find_all('div', {'class':"fc-item__header"})
        for element in elements:
            modules = element.find_all('a')
            for module in modules:
                link = str(module['href'])
                #print(link)
                links.append(link)

        return list(set(links))