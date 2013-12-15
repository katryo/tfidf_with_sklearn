from bing_api import Bing
import os
import constants
from web_page import WebPage

if __name__ == '__main__':
    bing = Bing()
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    results = bing.web_search(query=constants.QUERY, num_of_results=constants.NUM_OF_FETCHED_PAGES, keys=['Url'])
    for i, result in enumerate(results):
        page = WebPage(result['Url'])
        page.fetch_html()
        f = open('%s_%s.html' % (constants.QUERY, str(i)), 'w')
        f.write(page.html_body)
        f.close()
