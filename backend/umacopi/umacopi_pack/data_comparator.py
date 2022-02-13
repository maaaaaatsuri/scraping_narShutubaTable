

class DataComparator():
    def compare_data(self, new_data, old_data):

        if len(new_data) != len(old_data):
            return False
        else:
            for i in range(0, len(new_data)):
                if new_data[i] != old_data[i]:
                    return False
        return True