from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class AtlanticLinkFetcher(DownloadLinkFetcher):

    #1250
    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day+1128)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()
        # news links are the hrefs of a
        elements = soup.find_all('a', {'data-omni-click':"inherit"})
        for element in elements:
            # this a is not news link
            if element.get('rel', None) is not None:
                continue
            link = 'https://www.theatlantic.com'+str(element['href'])
            #print(link)
            links.append(link)

        return list(set(links))