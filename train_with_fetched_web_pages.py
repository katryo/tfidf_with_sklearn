import os
import pickle
import constants
from naive_bayes import NaiveBayes
import utils

if __name__ == '__main__':
    utils.go_to_fetched_pages_dir()
    pages = utils.load_html_files()
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