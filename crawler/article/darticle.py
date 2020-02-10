import sys
import os.path
import time
from datetime import timedelta

from network.network import NetworkFetcher
import xml.etree.ElementTree as ET
from xml.dom import minidom


class ArticleFetcher:

    RETRY = 5

    def __init__(self, config):
        self.config = config
        self.download_link_fetcher = None
        self.html_fetcher = NetworkFetcher()
        self.path = config.path

        self.total_date = 0

        self._mkdir(self.path,
                    config.start_date,
                    config.end_date,
                    config.step)

    def _mkdir(self, path, start_date, end_date, step):
        if os.path.isdir(path):
            # current_date = start_date
            # while current_date < end_date:
            #     current_date += step
            #     self.total_date += 1
            # return
            pass
        else:
            os.makedirs(path)
        current_date = start_date
        existed_years = dict()
        while current_date < end_date:
            year = current_date.year
            month = current_date.month
            day = current_date.day

            year_path = os.path.join(path, str(year))
            month_path = os.path.join(year_path, str(month))
            day_path = os.path.join(month_path, str(day))

            if year not in existed_years.keys():
                existed_years[year] = dict()
                if not os.path.isdir(year_path):
                    os.mkdir(year_path)

            if (step.months > 0) or (step.days > 0):
                year_content = existed_years[year]
                if month not in year_content.keys():
                    year_content[month] = True
                    if not os.path.isdir(month_path):
                        os.mkdir(month_path)

            if step.days > 0:
                if not os.path.isdir(day_path):
                    os.mkdir(day_path)
            current_date += step

            self.total_date += 1

    def _html_to_infomation(self, html, link, date):
        return {}

    def _extract_information(self, link, date):
        html = self.html_fetcher.fetch(link)
        if html is None:
            for _ in range(0, self.RETRY):
                html = self.html_fetcher.fetch(link)
                if html is not None:
                    break
        if html is None:
            print('article ', link, 'failed')
            return None
        return self._html_to_infomation(html, link, date)

    def _get_storage_path(self, path, date):
        return os.path.join(path, str(date.year), str(date.month), str(date.day))

    def _lazy_storage(self, storage_path, links, date):
        total_links = len(links)
        current_link = 1
        current_id = 1
        data = ET.Element('DATA')
        
        for link in links:
            print('>>> {c} in {t} articles\r'.format(c=current_link, t=total_links), end='')
            current_link += 1

            article = self._extract_information(link, date)
            
            if article is not None:
                article['ID']=str(article['ID'])+str(date)+'-'+str(current_id)
                #print(str(article['published_date']))

                docs = ET.SubElement(data, 'DOC')
                ID = ET.SubElement(docs, 'ID')
                theTitle = ET.SubElement(docs,'TITLE')
                auther = ET.SubElement(docs, 'AUTHER')
                timedate = ET.SubElement(docs, 'DATE')
                topic = ET.SubElement(docs, 'TOPIC')
                image = ET.SubElement(docs, 'IMAGE')
                content = ET.SubElement(docs,'TEXT')
                thelink = ET.SubElement(docs,'URL')   

                ID.text = str(article['ID'])
                theTitle.text = str(article['title'])
                auther.text = str(article['authors'])
                timedate.text = str(article['published_date'])
                topic.text = str(article['section'])
                image.text = str(article['image'])
                content.text = str(article['content'])
                thelink.text = str(article['link'])
                current_id += 1

        Prettyxml = minidom.parseString(ET.tostring(data)).toprettyxml(indent="   ")
        articles_path = os.path.join(storage_path, 'Articles.xml')
        with open(articles_path, mode='w', encoding='utf-8') as articles_file:
            articles_file.write(Prettyxml)

    def fetch(self, lazy_storage=True):
        current_date = 1
        while True:
            api_url, date = self.download_link_fetcher.next()
            #print(api_url)
            if api_url is None:
                break
            print(date.strftime('%Y-%m-%d'),
                  '{c} in {t} dates                  '.format(c=current_date, t=self.total_date))

            storage_path = self._get_storage_path(self.path, date)
            links = self.download_link_fetcher.fetch(api_url)
            self._lazy_storage(storage_path, links, date)
          
            time.sleep(self.config.sleep)

            print(date.strftime('%Y-%m-%d'),
                  'date {c} finished                 '.format(c=current_date))
            current_date += 1
