

class DateCreator():
    def create_date(self, year: int, month: int, day: int) -> str:
        date = str(year) + str('/') + str(month).zfill(2) + str('/') + str(day).zfill(2)

        return date # '2022/XX/XX'