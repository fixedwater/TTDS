import sys
import os.path

from dateutil.relativedelta import relativedelta

from settings.dataset_conf import DatasetConfiguration
from article.nytimes_article import NytimeArticleFetcher



if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please input configuration path')
    config = DatasetConfiguration()
    config.load(sys.argv[1])

    nytime_article_fetcher = NytimeArticleFetcher(config)
    nytime_article_fetcher.fetch()
