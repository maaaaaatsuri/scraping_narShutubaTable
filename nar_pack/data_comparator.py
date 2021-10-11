
class DataComparator():
    def compare_data(self, new_data, old_data):

        if len(new_data) != len(old_data):
            print('要素数に差異あり')
            return False

        else:
            for i in range(len(new_data) - 1):
                if new_data[i + 1] != old_data[i + 1]:
                    print('第1差異内容表示 -> ', 'new',new_data[i + 1], 'old',old_data[i + 1])
                    return False

        print('差異なし')
        return True