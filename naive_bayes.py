#coding:utf-8
# http://gihyo.jp/dev/serial/01/machine-learning/0003 のベイジアンフィルタ実装をPython3.3向けにリーダブルに改良
import math
import sys
import MeCab


class NaiveBayes:
    def __init__(self):
        self.vocabularies = set()
        self.word_count = {}  # {'花粉症対策': {'スギ花粉': 4, '薬': 2,...} }
        self.category_count = {}  # {'花粉症対策': 16, ...}

    def to_words(self, sentence):
        """
        入力: 'すべて自分のほうへ'
        出力: tuple(['すべて', '自分', 'の', 'ほう', 'へ'])
        """
        tagger = MeCab.Tagger('mecabrc')  # 別のTaggerを使ってもいい
        mecab_result = tagger.parse(sentence)
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
            words.append(info_elems[6])
        return tuple(words)

    def word_count_up(self, word, category):
        self.word_count.setdefault(category, {})
        self.word_count[category].setdefault(word, 0)
        self.word_count[category][word] += 1
        self.vocabularies.add(word)

    def category_count_up(self, category):
        self.category_count.setdefault(category, 0)
        self.category_count[category] += 1

    def train(self, doc, category):
        words = self.to_words(doc)
        for word in words:
            self.word_count_up(word, category)
        self.category_count_up(category)

    def prior_prob(self, category):
        num_of_categories = sum(self.category_count.values())
        num_of_docs_of_the_category = self.category_count[category]
        return num_of_docs_of_the_category / num_of_categories

    def num_of_appearance(self, word, category):
        if word in self.word_count[category]:
            return self.word_count[category][word]
        return 0

    def word_prob(self, word, category):
        # ベイズの法則の計算
        numerator = self.num_of_appearance(word, category) + 1  # +1は加算スムージングのラプラス法
        denominator = sum(self.word_count[category].values()) + len(self.vocabularies)

        # Python3では、割り算は自動的にfloatになる
        prob = numerator / denominator
        return prob

    def score(self, words, category):
        score = math.log(self.prior_prob(category))
        for word in words:
            score += math.log(self.word_prob(word, category))
        return score

    def classify(self, doc):
        best_guessed_category = None
        max_prob_before = -sys.maxsize
        words = self.to_words(doc)

        for category in self.category_count.keys():
            prob = self.score(words, category)
            if prob > max_prob_before:
                max_prob_before = prob
                best_guessed_category = category
        return best_guessed_category

if __name__ == '__main__':
    nb = NaiveBayes()
    nb.train('''Python（パイソン）は，オランダ人のグイド・ヴァンロッサムが作ったオープンソースのプログラミング言語。
                オブジェクト指向スクリプト言語の一種であり，Perlとともに欧米で広く普及している。イギリスのテレビ局 BBC が製作したコメディ番組『空飛ぶモンティパイソン』にちなんで名付けられた。
                Python は英語で爬虫類のニシキヘビの意味で，Python言語のマスコットやアイコンとして使われることがある。Pythonは汎用の高水準言語である。プログラマの生産性とコードの信頼性を重視して設計されており，核となるシンタックスおよびセマンティクスは必要最小限に抑えられている反面，利便性の高い大規模な標準ライブラリを備えている。
                Unicode による文字列操作をサポートしており，日本語処理も標準で可能である。多くのプラットフォームをサポートしており（動作するプラットフォーム），また，豊富なドキュメント，豊富なライブラリがあることから，産業界でも利用が増えつつある。
             ''',
             'Python')
    nb.train('''Ruby（ルビー）は，まつもとゆきひろ（通称Matz）により開発されたオブジェクト指向スクリプト言語であり，
                従来 Perlなどのスクリプト言語が用いられてきた領域でのオブジェクト指向プログラミングを実現する。
                Rubyは当初1993年2月24日に生まれ， 1995年12月にfj上で発表された。
                名称のRubyは，プログラミング言語Perlが6月の誕生石であるPearl（真珠）と同じ発音をすることから，
                まつもとの同僚の誕生石（7月）のルビーを取って名付けられた。
             ''',
             'Ruby')
    doc = 'グイド・ヴァンロッサムが作ったオープンソース'
    print('%s => 推定カテゴリ: %s' % (doc, nb.classify(doc)))  # 推定カテゴリ: Pythonになるはず

    doc = '純粋なオブジェクト指向言語です.'
    print('%s => 推定カテゴリ: %s' % (doc, nb.classify(doc)))  # 推定カテゴリ: Rubyになるはず



