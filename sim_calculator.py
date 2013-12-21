import math


class SimCalculator():
    def _absolute(self, vector):
        # ベクトルの長さつまり絶対値を返す
        squared_distance = sum([vector[word] * vector[word] for word in vector])
        distance = math.sqrt(squared_distance)
        return distance

    def sim_cos(self, v1, v2):
        numerator = 0
        # v1とv2で共通するkeyがあったとき、その値の積を加算していく。2つのベクトルの内積になる。
        for word in v1:
            if word in v2:
                numerator += v1[word] * v2[word]
        
        denominator = self._absolute(v1) * self._absolute(v2)

        if denominator == 0:
            return 0
        return numerator / denominator

    def sim_simpson(self, v1, v2):
        intersection = 0
        # v1とv2で共通するkeyの数を数えている
        for word in v2:
            if word in v1:
                intersection += 1
        denominator = min(len(v1), len(v2))

        # v1かv2の中身が0だったとき
        if denominator == 0:
            return 0
        return intersection / denominator

if __name__ == '__main__':
    sc = SimCalculator()
    print('コサイン類似度は' + str(sc.sim_cos({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1})))
    print('シンプソン係数で計算した類似度は' + str(sc.sim_simpson({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1})))

