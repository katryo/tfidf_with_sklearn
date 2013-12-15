import requests
import pdb
import cchardet
import re


class WebPage():
    def __init__(self, url=''):
        self.url = url

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            self.set_html_body_with_cchardet(response)
        except ConnectionError:
            self.html_body = ''

    def set_html_body_with_cchardet(self, response):
        encoding_detected_by_cchardet = cchardet.detect(response.content)['encoding']
        response.encoding = encoding_detected_by_cchardet
        self.html_body = response.text

    def remove_html_tags(self):
        html_tag_pattern = re.compile('<.*?>')
        self.html_body = html_tag_pattern.sub('', self.html_body)