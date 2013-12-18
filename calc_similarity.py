from sim_calculator import SimCalculator
from naive_bayes import NaiveBayes
import constants
import pickle
import sys

if __name__ == '__main__':
    sc = SimCalculator()
    with open(constants.NB_PKL_FILENAME, 'rb') as f:
        nb_classifier = pickle.load(f)

    # 標準入力した文字列を、trainとword_countを使って {'input': {'スギ花粉': 4, '薬':3}}という形式に整形するためNBオブジェクトにした
    # 分類器としては使わないので本当は別のクラスを作ってやるべき。だがめんどいのでNBオブジェクトにする。
    nb_input = NaiveBayes()

    for query in sys.stdin:
        nb_input.word_count = {}  # 二回目以降のinputのための初期化
        nb_input.train(query, 'input')
        for category in nb_classifier.word_count:
            sim_cos = sc.sim_cos(nb_input.word_count['input'], nb_classifier.word_count[category])
            print('カテゴリー「%s」との類似度は %f です' % (category, sim_cos))
