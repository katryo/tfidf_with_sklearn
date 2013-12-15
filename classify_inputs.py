import pickle
import constants
import sys
import pdb

if __name__ == '__main__':
    with open(constants.NB_PKL_FILENAME, 'rb') as f:
        nb = pickle.load(f)
    for query in sys.stdin:
        result = nb.classify(query)
        print(result)