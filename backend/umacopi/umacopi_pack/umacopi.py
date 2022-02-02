from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from utils import Utils
from date_creator import DateCreator
from venue_code_creator import VenueCodeCreator
from reverse_number_adder import ReverseNumberAdder
from race_number_adder import RaceNumberAdder
from type_changer import TypeChanger
from db_manager import DbManager
import pandas as pd
import time
import sqlite3
import sys


# レース情報分析クラス(コマンドライン引数に["開催場所"、"年"、"月"、"日"、"レースナンバー"]を入力)
class RaceInfoAnalyzer():
    def __init__(self, venue, year, month, day, race_num):
        self.venue = venue
        self.year = year
        self.month = month
        self.day = day
        self.race_num = race_num

        # 開催場所コード作成
        venue_code_creator = VenueCodeCreator()
        self.venue_dict = venue_code_creator.fetch_venue_dict()
        self.selected_venue = self.venue_dict[self.venue]

        # 開催日データ作成(ex.2022/XX/XX)
        date_creator = DateCreator()
        self.date = date_creator.create_date(year, month, day)

        self.shutuba_table = pd.DataFrame()
        self.type_changer = TypeChanger()
        self.db_manager = DbManager(self.venue, self.date)

# =======================================出馬表スクレイピング========================================================
    def scraping_shutuba_table(self):
        race_id = str(self.year) + str(self.selected_venue).zfill(2) + str(self.month).zfill(2) + str(self.day).zfill(2) + str(self.race_num).zfill(2)
        race_id = int(race_id)

        self.race_id_lst = []
        race_counts = self.race_num
        while race_counts <= 12:
            self.race_id_lst.append(race_id)
            race_id += 1
            race_counts += 1
            
        # 出馬表を取得
        self.shutuba_table = pd.DataFrame()
        # ヘッドレス解除コード
        # self.browser = webdriver.Chrome(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--headless')
        options.add_argument('no-sandbox')
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        time.sleep(1)
        
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=' + str(race_id)
            self.browser.get(url)
            time.sleep(1)
            elems = self.browser.find_elements_by_class_name('HorseList')
            for elem in elems:
                tds = elem.find_elements_by_tag_name('td')
                row = []
                for td in tds:
                    row.append(td.text)
                self.shutuba_table = self.shutuba_table.append(pd.Series(row, name=race_id))

        columns_name_list = ['frame','umaban','mark','horse_name','age','weight','jockey','stable','horse_weight(fluctuated)','odds','popularity','','']
        combined_columns = [columns_name_list[0:len(self.shutuba_table.columns + 1)]]
        combined_columns = list(Utils.flatten_2d(combined_columns))
        
        self.shutuba_table.columns = [x for x in combined_columns]

        # 開催日カラム追加
        self.shutuba_table['date'] = self.date

        # 開催場所カラム追加
        venue_dict_swap = {v: k for k, v in self.venue_dict.items()}
        self.shutuba_table['venue'] = venue_dict_swap[self.selected_venue]

        # レース(番号)カラム追加
        race_number_adder = RaceNumberAdder()
        self.shutuba_table = race_number_adder.add_race_number(self.shutuba_table)

        # 着順(空値)カラム追加
        self.shutuba_table['rank'] = '--'

        # 逆番カラム追加
        reverse_number_adder = ReverseNumberAdder()
        self.shutuba_table = reverse_number_adder.add_reverse_number(self.shutuba_table)

        # 対象のカラムのデータ型をDBに合わせて変換
        self.shutuba_table['frame'] = self.type_changer.change_to_int(self.shutuba_table['frame'])
        self.shutuba_table['umaban'] = self.type_changer.change_to_int(self.shutuba_table['umaban'])
        self.shutuba_table['popularity'] = self.type_changer.change_to_int(self.shutuba_table['popularity'])
        self.shutuba_table['odds'] = self.type_changer.change_to_float(self.shutuba_table['odds'])

        self.shutuba_table = self.shutuba_table[[
            'date','venue','race_number','rank','frame','umaban','rev_umaban',
            'mark','horse_name','jockey','stable','odds','popularity'
            ]]
        self.shutuba_table = self.shutuba_table.reset_index(drop=True)
        print('='*5,'【 出 馬 表 】','='*85, '\n', self.shutuba_table)

        return self.shutuba_table
# =====================================レース結果スクレイピング========================================================
    # 着順を取得
    def scraping_race_result(self):
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/result.html?race_id=' + str(race_id)
            self.browser.get(url)
            time.sleep(1)
            horse_names = self.browser.find_elements_by_class_name("Horse_Name")
            h_name_lst = [h.text for h in horse_names if h.text != '馬名']

            ranks = self.browser.find_elements_by_class_name("Rank")
            rank_lst = [r.text for r in ranks]

            name_rank_dict = dict(zip(h_name_lst, rank_lst))
            for k in name_rank_dict.keys():
                i = 0
                while k != self.shutuba_table['horse_name'][i]:
                    i += 1
                self.shutuba_table['rank'][i] = self.type_changer.result_int(name_rank_dict[k])
        print('='*5,'【 レ ー ス 結 果 】','='*80, '\n', self.shutuba_table, '\n')

        self.browser.quit()
        self.db_manager.save_db(self.shutuba_table)
        return self.shutuba_table


if __name__ == '__main__':
    args = sys.argv
    raceinfo = RaceInfoAnalyzer(args[1], args[2], args[3], args[4], int(args[5]))
    raceinfo.scraping_shutuba_table()
    raceinfo.scraping_race_result()