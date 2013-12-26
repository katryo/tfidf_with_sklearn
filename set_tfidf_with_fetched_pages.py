import utils
from math import log
import pdb
import constants

def num_of_docs_with_term(pages, word):
    count = 1  # 1はスムージング
    for page in pages:
        if word in page.terms:
            count += 1
    return count


def set_tfidf(pages, page, word):
    term = page.terms[word]
    term.df = num_of_docs_with_term(pages, word) / len(pages)
    if not constants.MIN_DF < term.df < constants.MAX_DF:
        term.tfidf = 0
        return
    term.idf = log(1 / term.df)
    term.tfidf = term.tf / term.idf
    if term.tfidf > 0.000001:
        print('%s, %f' % (word, term.tfidf))

if __name__ == '__main__':
    utils.go_to_fetched_pages_dir()
    pages = utils.load_all_html_files()  # pagesはhtmlをフェッチしてtextにセットずみ
    pdb.set_trace()
    for page in pages:
        page.set_words_from_text()
        page.set_terms_from_words()
        page.set_terms_tf()

    # すべてのpageにtermsをセットし終わってからdfを計算する

    for page in pages:
        for word in page.terms:
            set_tfidf(pages, page, word)

