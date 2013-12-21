import math


class SimCalculator():
    def _distance(self, v1, v2):
        #ピタゴラスの定理（次元の一般化により3以上の次元でも通用）で距離を計算
        sum_of_squared_values = lambda vector: sum([vector[word] * vector[word] for word in vector])
        squared_distance = sum_of_squared_values(v1) * sum_of_squared_values(v2)
        distance = math.sqrt(squared_distance)
        return distance

    def sim_cos(self, v1, v2):
        numerator = 0
        # v1とv2で共通するkeyがあったとき、その値の積を加算していく
        for word in v1:
            if word in v2:
                numerator += v1[word] * v2[word]
        
        denominator = self._distance(v1, v2)

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
    print(sc.sim_cos({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1}))
    print(sc.sim_simpson({'ライフハック': 1, '骨折': 2}, {'ライフハック': 2, '仕事': 1, '趣味': 1}))

