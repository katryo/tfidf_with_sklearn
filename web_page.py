import requests
import cchardet
import re
import utils
import pdb
from term import Term

class WebPage():
    def __init__(self, url=''):
        self.url = url
        self.terms = {}

    def fetch_html(self):
        try:
            response = requests.get(self.url)
            self.set_html_body_with_cchardet(response)
        except requests.exceptions.ConnectionError:
            self.html_body = ''

    def set_html_body_with_cchardet(self, response):
        encoding_detected_by_cchardet = cchardet.detect(response.content)['encoding']
        response.encoding = encoding_detected_by_cchardet
        self.html_body = response.text

    def remove_html_tags(self):
        html_tag_pattern = re.compile('<.*?>')
        semicolon_pattern = re.compile(';\n')
        script_tag_pattern = re.compile('<script.*?</script>')
        break_pattern = re.compile('\n')
        tab_pattern = re.compile('\t')
        brace_pattern = re.compile('\{.*?\}')
        text = semicolon_pattern.sub('', self.html_body)
        text = script_tag_pattern.sub('', text)
        text = tab_pattern.sub('', text)
        text = break_pattern.sub('', text)
        text = brace_pattern.sub('', text)
        self.text = html_tag_pattern.sub('', text)

    def term_count_up(self, word):
        self.terms.setdefault(word, Term(word))  # terms == {'薬': Term('薬')}
        self.terms[word].count_up()

    def set_words_from_text(self):
        self.words = utils.words(self.text)

    def set_terms_from_words(self):
        # self.remove_html_tagsをしていることが前提
        self.words_count = len(self.words)
        for word in self.words:
            self.term_count_up(word)

    def set_terms_tf(self):
        for word in self.terms:
            term = self.terms[word]
            term.set_tf(self.words_count)