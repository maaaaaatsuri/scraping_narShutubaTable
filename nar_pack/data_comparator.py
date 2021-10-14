

class DataComparator():
    def compare_data(self, new_data, old_data):

        if len(new_data) != len(old_data):
            return False
        else:
            for i in range(1, len(new_data)):
                if new_data[i] != old_data[i]:
                    print('第1差異内容 ->', ' 更新前=',old_data[i], ',  更新後=',new_data[i])
                    return False
        return True