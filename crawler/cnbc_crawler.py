import sys
import os.path

from dateutil.relativedelta import relativedelta

from settings.dataset_conf import DatasetConfiguration
from article.cnbc_article import CnbcArticleFetcher



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please input configuration path')
    config = DatasetConfiguration()
    config.load(sys.argv[1])

    Cnbc_article_fetcher =  CnbcArticleFetcher(config)
    Cnbc_article_fetcher.fetch()
