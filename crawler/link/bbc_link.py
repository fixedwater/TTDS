from bs4 import BeautifulSoup

from .dlink import DownloadLinkFetcher



class BBCLinkFetcher(DownloadLinkFetcher):

    BBC_FILTERS = [
        ['programmes', 21, 31],
        ['correspondents', 26, 40],
        ['iplayer', 21, 28],
        ['radio', 21, 26],
        ['live', 27, 31],
        ['m', 7, 8]
    ]

    def _next_api(self, base_url, current_date):
        year = current_date.year
        month = current_date.month
        day = current_date.day
        api_url = base_url.format(year=year, month=month, day=day)
        return api_url

    def _html_to_links(self, html):
        soup = BeautifulSoup(html, 'lxml')

        links = list()

        '''
        elements = soup.find_all('a',{'class' : 'faux-block-link__overlay'})
        
        #elements = soup.find_all('a',{'class' : 'gs-c-promo-heading gs-o-faux-block-link__overlay-link sp-o-link-split__anchor gel-pica-bold'})
        for element in elements:
            link = 'https://www.bbc.co.uk'+str(element['href'])
            #print(link)
            links.append(link)
        '''

        
        '''
        elements = soup.find_all('div',{'id' : 'tl_1'})
        for module in elements:
            infos = module.find_all('a')
            for info in infos:
                link = str(info['href'])
                #print(link)
                links.append(link)
        '''
        
            
        # news links are the hrefs of a
        elements = soup.table.find_all('a')
        for element in elements:
            # this a is not news link
            if element.get('rel', None) is not None:
                continue
            link = self._format_link(element['href'])
            if self._link_filter(link, self.BBC_FILTERS):
                links.append(link)
        

        return list(set(links))
