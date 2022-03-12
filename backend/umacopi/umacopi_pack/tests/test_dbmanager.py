import pytest
import pandas as pd
import os
import sys

rootdir = os.path.dirname(os.path.dirname(__file__))
sys.path.extend([rootdir])

from data_comparator import DataComparator
from db_manager import DbManager



# ===== DbManagerテスト
data_comparator = DataComparator()
@pytest.mark.parametrize("new, old, bool",[
    ([1, 2, 3], [7, 8, 9], False),
    (['a','b','c'], ['a','b','c'], True),
])
def test_compare_data(new, old, bool) -> bool:
    result = data_comparator.compare_data(new, old)
    assert result == bool

df = pd.DataFrame({'date': ['2022/test/test', '2022/test/test'],
                   'venue': ['test競馬場', 'test競馬場'],
                   'race_number': ['test_race_number1', 'test_race_number2'],
                   'rank': ['test_rank1', 'test_rank2'],
                   'frame': ['test_frame1', 'test_frame2'],
                   'umaban': ['test_umaban1', 'test_umaban2'],
                   'rev_umaban': ['test_rev_umaban1', 'test_rev_umaban2'],
                   'mark': ['test_markA', 'test_markB'],
                   'horse_name': ['test_horse_nameA', 'test_horse_nameB'],
                   'jockey': ['test_jockey1', 'test_jockey2'],
                   'stable': ['test_stable1', 'test_stable2'],
                   'odds': ['test_odds10', 'test_odds20'],
                   'popularity': ['test_popularity1', 'test_popularity2']},
                  index=['test_row0', 'tets_row1'])
db_manager = DbManager('/root/test/umacopi/web/db.sqlite3')
def test_save_db() -> None:
    result = db_manager.save_db('test競馬場', '2022/test/test', df)
    assert result == 0