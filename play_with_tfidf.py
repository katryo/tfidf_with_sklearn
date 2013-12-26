# -*- coding: utf-8 -*-
import pickle
import constants
import pdb

def is_bigger_than_min_tfidf(term, terms, tfidfs):
    '''
    [term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)]で使う
    list化した、語たちのtfidfの値のなかから、順番に当てる関数。
    tfidfの値がMIN_TFIDFよりも大きければTrueを返す
    '''
    if tfidfs[terms.index(term)] > constants.MIN_TFIDF:
        return True
    return False

if __name__ == '__main__':
    with open(constants.TFIDF_VECTORIZER_PKL_FILENAME, 'rb') as f:
        vectorizer = pickle.load(f)
    with open(constants.TFIDF_RESULT_PKL_FILENAME, 'rb') as f:
        x = pickle.load(f)

    pdb.set_trace()

    terms = vectorizer.get_feature_names()
    for i in range(3):
        tfidfs = x.toarray()[i]
        print([term for term in terms if is_bigger_than_min_tfidf(term, terms, tfidfs)])