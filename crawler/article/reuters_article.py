from bs4 import BeautifulSoup
from goose3 import Goose
from datetime import datetime
from .darticle import ArticleFetcher
from link.reuters_link import ReutersLinkFetcher


class ReutersArticleFetcher(ArticleFetcher):

    def __init__(self, config):
        super(ReutersArticleFetcher, self).__init__(config)
        self.download_link_fetcher = ReutersLinkFetcher(config)

    def _extract_title(self, soup):
        return soup.title.get_text()

    def _extract_published_date(self, soup):
        #return date.strftime('%Y-%m-%d')
        published = soup.find('meta',{'name':"analyticsAttributes.articleDate"})
        date = published['content']
        return '-'.join([date[:4], date[5:7], date[8:10]])
        #return published['content']

    def _extract_authors(self, soup):
        authors_elements = soup.find('meta', property="og:article:author")
        return authors_elements['content']

    def _extract_description(self, soup):
        description_element = soup.find('meta', property='og:description')
        return description_element['content']

    def _extract_section(self, soup):
        section_element = soup.find('meta', property="og:article:section")
        return section_element['content']

    def _extract_content(self, html):
        g = Goose({'enable_image_fetching': False})
        article = g.extract(raw_html=html)
        return article.cleaned_text

    def _extract_id(self):
        i = "reuter"
        return i

    def _extract_image(self,soup):
        image = soup.find('meta',property="og:image")
        return image['content']

    def _html_to_infomation(self, html, link, date):
        soup = BeautifulSoup(html, 'lxml')
        head = soup

        try:
            title = self._extract_title(head)
            published_date = self._extract_published_date(head)
            authors = self._extract_authors(head)
            description = self._extract_description(head)
            section = self._extract_section(head)
            content = self._extract_content(html)
            id = self._extract_id()
            image = self._extract_image(head)
        except Exception as err:
            print(err)
            return None

        return {
            'title': title,
            'ID':id,
            'published_date': published_date,
            'authors': authors,
            'description': description,
            'section': section,
            'content': content,
            'link': link,
            'image':image
        }
