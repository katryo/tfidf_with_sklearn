import MeCab
import constants
import os
import pdb
from web_page import WebPage

def _split_to_words(text, to_stem=False):
    """
    入力: 'すべて自分のほうへ'
    出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
    """
    tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
    mecab_result = tagger.parse(text)
    info_of_words = mecab_result.split('\n')
    words = []
    for info in info_of_words:
        # macabで分けると、文の最後に’’が、その手前に'EOS'が来る
        if info == 'EOS' or info == '':
            break
            # info => 'な\t助詞,終助詞,*,*,*,*,な,ナ,ナ'
        info_elems = info.split(',')
        # 6番目に、無活用系の単語が入る。もし6番目が'*'だったら0番目を入れる
        if info_elems[6] == '*':
            # info_elems[0] => 'ヴァンロッサム\t名詞'
            words.append(info_elems[0][:-3])
            continue
        if to_stem:
            # 語幹に変換
            words.append(info_elems[6])
            continue
        # 語をそのまま
        words.append(info_elems[0][:-3])
    return words


def words(text):
    words = _split_to_words(text, to_stem=False)
    return words


def stems(text):
    stems = _split_to_words(text, to_stem=True)
    return stems


def load_all_html_files():
    pages = []
    for query in constants.QUERIES:
        pages.extend(load_html_files_with_query(query))
    return pages


def load_html_files_with_query(query):
    pages = []
    for i in range(constants.NUM_OF_FETCHED_PAGES):
        with open('%s_%s.html' % (query, str(i)), 'r') as f:
            page = WebPage()
            page.html_body = f.read()
        page.remove_html_tags()
        pages.append(page)
    return pages

def load_html_files():
    """
    HTMLファイルがあるディレクトリにいる前提で使う
    """
    pages = load_html_files_with_query(constants.QUERY)
    return pages


def go_to_fetched_pages_dir():
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
