

class DateCreator():
    def create_date(self, year, month, day):
        date = str(year) + str('/') + str(month).zfill(2) + str('/') + str(day).zfill(2)

        return date