import sys

from settings.dataset_conf import DatasetConfiguration
from article.atlantic_article import AtlanticArticleFetcher


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('please input configuration path')
    config = DatasetConfiguration()
    config.load(sys.argv[1])

    at_article_fetcher = AtlanticArticleFetcher(config)
    at_article_fetcher.fetch()