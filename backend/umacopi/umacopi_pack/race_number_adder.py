

class RaceNumberAdder():
    def add_race_number(self, data):
        i_lst = []
        for i in data.index:
            i_lst.append(str(i)[-2:])
        data.index = i_lst

        data = data.rename(index={
            '01': '01R', '02': '02R',
            '03': '03R', '04': '04R',
            '05': '05R', '06': '06R',
            '07': '07R', '08': '08R',
            '09': '09R', '10': '10R',
            '11': '11R', '12': '12R'
            })

        data['race_number'] = data.index
        return data