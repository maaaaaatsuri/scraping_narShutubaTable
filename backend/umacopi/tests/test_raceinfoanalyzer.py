import pytest
import pandas as pd
from umacopi_pack.date_creator import DateCreator
from umacopi_pack.race_number_adder import RaceNumberAdder


# ===== RaceInfoAnalyzerテスト
date_creator = DateCreator()
@pytest.mark.parametrize("year, month, day, date",[
    (2022, 5, 10, '2022/05/10'),
    (2024, 10, 1, '2024/10/01'),
])
def test_create_date(year, month, day, date) -> str:
    result = date_creator.create_date(year, month, day)
    assert result == date

# race_number_adder = RaceNumberAdder()
# df = pd.DataFrame({'date': ['2022/test/test', '2022/test/test'],
#                    'venue': ['test競馬場', 'test競馬場'],
#                    'race_number': ['test_race_number1', 'test_race_number2'],
#                    'rank': ['test_rank1', 'test_rank2'],
#                    'frame': ['test_frame1', 'test_frame2'],
#                    'umaban': ['test_umaban1', 'test_umaban2'],
#                    'rev_umaban': ['test_rev_umaban1', 'test_rev_umaban2'],
#                    'mark': ['test_markA', 'test_markB'],
#                    'horse_name': ['test_horse_nameA', 'test_horse_nameB'],
#                    'jockey': ['test_jockey1', 'test_jockey2'],
#                    'stable': ['test_stable1', 'test_stable2'],
#                    'odds': ['test_odds10', 'test_odds20'],
#                    'popularity': ['test_popularity1', 'test_popularity2']},
#                   index=['0001', '0002'])
# def test_add_race_number() -> str:
#     result = race_number_adder.add_race_number(df)
#     result = result.index
#     assert result == '01R'

