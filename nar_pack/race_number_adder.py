

class RaceNumberAdder():
    def add_race_number(self, data):
        i_lst = []
        for i in data.index:
            i_lst.append(str(i)[-2:])
        data.index = i_lst

        data = data.rename(index={
            '01': '1R', '02': '2R',
            '03': '3R', '04': '4R',
            '05': '5R', '06': '6R',
            '07': '7R', '08': '8R',
            '09': '9R', '10': '10R',
            '11': '11R', '12': '12R'
            })

        data['レース'] = data.index
        return data