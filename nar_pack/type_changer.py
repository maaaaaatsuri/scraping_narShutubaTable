

class TypeChanger():

    def change_to_int(self, data):
        int_data = [int(datum) if datum.isdecimal() else '--' for datum in data]
        data = int_data
        return data

    def change_to_float(self, data):
        float_data = []
        for datum in data:
            try:
                datum = float(datum)
                float_data.append(datum)
            except ValueError:
                float_data.append('--')
        return float_data

    def result_int(self, data):
        try:
            data = int(data)
        except ValueError:
            data = '--'
        return data