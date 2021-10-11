from python_utils.utils import Utils
from typing import *


class ReverseNumberAdder():
    # 逆番カラム追加メソッド
    def add_reverse_number(self, data):
        indiv_rev_num = []
        all_rev_num = []
        temp = 1
        for value in data.index:
            while value:
                if temp == 1 or value == previous_value:
                    indiv_rev_num.append(temp)
                    temp += 1
                elif value != previous_value:
                    temp = 1
                    all_rev_num.append(indiv_rev_num[::-1])
                    indiv_rev_num.clear()
                    indiv_rev_num.append(temp)
                    temp += 1

                previous_value = value
                value = False
        all_rev_num.append(indiv_rev_num[::-1])

        all_rev_num = list(Utils.flatten_2d(all_rev_num))
        data['逆番'] = all_rev_num
        return data