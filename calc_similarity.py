from sim_calculator import SimCalculator
from naive_bayes import NaiveBayes
import constants
import pickle
import sys
import pdb
from collections import OrderedDict


if __name__ == '__main__':
    sc = SimCalculator()
    with open(constants.NB_PKL_FILENAME, 'rb') as f:
        nb_classifier = pickle.load(f)

    # 標準入力した文字列を、trainとword_countを使って {'input': {'スギ花粉': 4, '薬':3}}という形式に整形するためNBオブジェクトにした
    # 分類器としては使わないので本当は別のクラスを作ってやるべきだがめんどい
    nb_input = NaiveBayes()

    for query in sys.stdin:
        nb_input.word_count = {}  # 二回目以降のinputのための初期化
        nb_input.train(query, 'input')
        results = OrderedDict()
        for category in nb_classifier.word_count:
            sim_cos = sc.sim_cos(nb_input.word_count['input'], nb_classifier.word_count[category])
            results[category] = sim_cos  # 最高valueのkeyを求めるためtupleにした

        for result in results:
            print('カテゴリー「%s」との類似度は %f です' % (result, results[result]))

        # http://cointoss.hatenablog.com/entry/2013/10/16/123129
        best_score_before = 0.0
        best_category = ''
        for i, category in enumerate(results):
            if results[category] > best_score_before:
                best_category = category
                best_score_before = results[category]
        print('類似度の最も高いカテゴリーは「%s」で類似度は %f です' % (best_category, results[best_category]))
