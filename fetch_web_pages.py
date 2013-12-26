from bing_api import Bing
import constants
from web_page import WebPage
import utils

if __name__ == '__main__':
    bing = Bing()
    utils.go_to_fetched_pages_dir()
    results = bing.web_search(query=constants.QUERY, num_of_results=constants.NUM_OF_FETCHED_PAGES, keys=['Url'])
    for i, result in enumerate(results):
        page = WebPage(result['Url'])
        page.fetch_html()
        with open('%s_%i.html' % (constants.QUERY, i), 'w') as f:
            f.write(page.html_body)
            print('%s_%i.htmlを%sに保存しました。' % (constants.QUERY, i, constants.FETCHED_PAGES_DIR_NAME))
