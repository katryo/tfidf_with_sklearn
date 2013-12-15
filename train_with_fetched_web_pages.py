import os
import pickle
import constants
from web_page import WebPage
from naive_bayes import NaiveBayes


def load_html_files():
    """
    HTMLファイルがあるディレクトリにいる前提で使う
    """
    pages = []
    for i in range(constants.NUM_OF_FETCHED_PAGES):
        with open('%s_%s.html' % (constants.QUERY, str(i)), 'r') as f:
            page = WebPage()
            page.html_body = f.read()
        page.remove_html_tags()
        pages.append(page)
    return pages

if __name__ == '__main__':
    # もういちど別の場所で使うのなら関数にする
    if not os.path.exists(constants.FETCHED_PAGES_DIR_NAME):
        os.mkdir(constants.FETCHED_PAGES_DIR_NAME)
    os.chdir(constants.FETCHED_PAGES_DIR_NAME)
    pages = load_html_files()
    pkl_nb_path = os.path.join('..', constants.NB_PKL_FILENAME)

    # もしすでにNaiveBayesオブジェクトをpickle保存していたらそれを学習させる
    if os.path.exists(pkl_nb_path):
        with open(pkl_nb_path, 'rb') as f:
            nb = pickle.load(f)
    else:
        nb = NaiveBayes()
    for page in pages:
        nb.train(page.html_body, constants.QUERY)
    # せっかく学習させたんだから保存しよう
    with open(pkl_nb_path, 'wb') as f:
        pickle.dump(nb, f)