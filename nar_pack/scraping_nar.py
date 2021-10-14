from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from venue_code_creator import VenueCodeCreator
from reverse_number_adder import ReverseNumberAdder
from race_number_adder import RaceNumberAdder
from data_comparator import DataComparator
from type_changer import TypeChanger
import time
import sqlite3
import sys


# レース情報分析クラス(コマンドライン引数に["開催場所"、"年"、"月"、"日"、"レースナンバー"]を入力)
class RaceInfoAnalyzer():
    def __init__(self, venue):
        self.shutuba_table = pd.DataFrame()

        venue_code_creator = VenueCodeCreator()
        self.venue_dict = venue_code_creator.fetch_venue_dict()
        self.selected_venue = self.venue_dict[venue]
        self.type_changer = TypeChanger()
# =======================================出馬表スクレイピング========================================================
    def scraping_shutuba_table(self, year, month, day, race_num):
        
        self.date = str(year) + str('/') + str(month).zfill(2) + str('/') + str(day).zfill(2)
        race_id = str(year) + str(self.selected_venue).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(race_num).zfill(2)
        race_id = int(race_id)
        
        self.race_id_lst = []
        race_counts = race_num
        while race_counts <= 12:
            self.race_id_lst.append(race_id)
            race_id += 1
            race_counts += 1
            
        # 出馬表を取得
        self.shutuba_table = pd.DataFrame()
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
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
        self.shutuba_table.columns = [
            '枠','馬番','印','馬名','性齢','斤量','騎手',
            '厩舎','馬体重(増減)','単勝オッズ','人気','',''
            ]

        # 開催日カラム追加
        self.shutuba_table['開催日'] = self.date

        # 開催場所カラム追加
        venue_dict_swap = {v: k for k, v in self.venue_dict.items()}
        self.shutuba_table['開催場所'] = venue_dict_swap[self.selected_venue]

        # レース(番号)カラム追加
        race_number_adder = RaceNumberAdder()
        self.shutuba_table = race_number_adder.add_race_number(self.shutuba_table)

        # 着順(空値)カラム追加
        self.shutuba_table['着順'] = '--'

        # 逆番カラム追加
        reverse_number_adder = ReverseNumberAdder()
        self.shutuba_table = reverse_number_adder.add_reverse_number(self.shutuba_table)

        # 対象カラムのデータ型をDBに合わせて変換
        self.shutuba_table['枠'] = self.type_changer.change_to_int(self.shutuba_table['枠'])
        self.shutuba_table['馬番'] = self.type_changer.change_to_int(self.shutuba_table['馬番'])
        self.shutuba_table['人気'] = self.type_changer.change_to_int(self.shutuba_table['人気'])
        self.shutuba_table['単勝オッズ'] = self.type_changer.change_to_float(self.shutuba_table['単勝オッズ'])

        self.shutuba_table = self.shutuba_table[[
            '開催日','開催場所','レース','着順','枠','馬番','逆番',
            '印','馬名','騎手','厩舎','単勝オッズ','人気'
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
                while k != self.shutuba_table['馬名'][i]:
                    i += 1
                self.shutuba_table['着順'][i] = self.type_changer.result_int(name_rank_dict[k])
        print('='*5,'【 レ ー ス 結 果 】','='*80, '\n', self.shutuba_table, '\n')

        self.browser.quit()
        return self.shutuba_table
# ==================================================DBに保存=========================================================
    def save_db(self):
        db_name = 'nar.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        data_comparator = DataComparator()
        for new_row in self.shutuba_table.itertuples(name=None):
            sql_select = 'SELECT * FROM nar WHERE 開催日 = ? AND 馬名 = ?'
            unique_key = (new_row[1], new_row[9])

            old_row = cur.execute(sql_select, unique_key)
            old_row = old_row.fetchall()

            if old_row == []:
                sql_insert = 'INSERT INTO nar ([開催日],[開催場所],[レース],[着順],[枠],[馬番],[逆番],[印],[馬名],[騎手],[厩舎],[単勝オッズ],[人気]) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
                new_row_data = (
                    new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6],
                    new_row[7], new_row[8], new_row[9], new_row[10], new_row[11], new_row[12], new_row[13]
                    )
                print('insert ->', new_row_data)
                cur.execute(sql_insert, new_row_data)

            else:
                old_row = old_row[0]
                if not data_comparator.compare_data(new_row, old_row):
                    sql_update = 'UPDATE nar SET 着順 = ?, 印 = ?, 騎手 = ?, 単勝オッズ = ?, 人気 = ?  WHERE 開催日 = ? AND 馬名 = ?'
                    update_data = (new_row[4], new_row[8], new_row[10], new_row[12], new_row[13],   new_row[1], new_row[9])                    
                    print('update ->', update_data, '\n')
                    cur.execute(sql_update, update_data)
                else:
                    pass

        conn.commit()
        conn.close()



if __name__ == '__main__':
    args = sys.argv
    hoge = RaceInfoAnalyzer(args[1])
    hoge.scraping_shutuba_table(args[2], args[3], args[4], int(args[5]))
    hoge.scraping_race_result()
    hoge.save_db()
