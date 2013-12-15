# -*- coding: utf-8 -*-
import pickle
import constants
import sys

if __name__ == '__main__':
    with open(constants.NB_PKL_FILENAME, 'rb') as f:
        nb = pickle.load(f)
    for query in sys.stdin:
        result = nb.classify(query)
        print('推測されたカテゴリーは %s です' % result)
