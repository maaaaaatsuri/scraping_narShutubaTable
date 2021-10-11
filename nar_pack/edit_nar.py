from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from venue_code_creator import VenueCodeCreator
from reverse_number_adder import ReverseNumberAdder
from race_number_adder import RaceNumberAdder
from data_comparator import DataComparator

import time
import  sqlite3


# レース情報分析クラス
class RaceInfoAnalyzer():
    def __init__(self, venue):
        self.shutuba_table = pd.DataFrame()

        venue_code_creator = VenueCodeCreator()
        self.venue_dict = venue_code_creator.fetch_venue_dict()
        self.selected_venue = self.venue_dict[venue]
# =======================================出馬表スクレイピング========================================================
    # 出馬表スクレイピング関数、引数に("年"、"selected_code"、"月"、"日"、"レースナンバー")を入力
    def scraping_shutuba_table(self, year, month, day, race_num):
        
        self.date = str(year) + str('/') + str(month).zfill(2) + str('/') + str(day).zfill(2)
        # self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d")
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
        self.venue_dict_swap = {v: k for k, v in self.venue_dict.items()}
        self.shutuba_table['開催場所'] = self.venue_dict_swap[self.selected_venue]

        # レース(番号)カラム追加
        race_number_adder = RaceNumberAdder()
        self.shutuba_table = race_number_adder.add_race_number(self.shutuba_table)

        # 着順(空値)カラム追加
        self.shutuba_table['着順'] = '--'

        # 逆番カラム追加
        reverse_number_adder = ReverseNumberAdder()
        self.shutuba_table = reverse_number_adder.add_reverse_number(self.shutuba_table)

        
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
            horse_Names = self.browser.find_elements_by_class_name("Horse_Name")
            h_ls = [h.text for h in horse_Names if h.text != '馬名']

            ranks = self.browser.find_elements_by_class_name("Rank")
            r_ls = [r.text for r in ranks]

            rh_dict = dict(zip(h_ls, r_ls))
            
            for k in rh_dict.keys(): # {馬名: 着順}から馬名を取り出し、出馬表と照合。馬名が一致するまでホイールし、一致したら着順補填。
                i = 0
                while k != self.shutuba_table['馬名'][i]:
                    i += 1
                self.shutuba_table['着順'][i] = rh_dict[k]
        print('='*5,'【 レ ー ス 結 果 】','='*80, '\n', self.shutuba_table)

        self.browser.quit()
        return self.shutuba_table
# =====================================DB========================================================
    def save_db(self):
        db_name = 'nar.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()

        data_comparator = DataComparator()
        for new_row in self.shutuba_table.itertuples(name=None): # スクレイピングした出馬表から1行ずつ取得(tuple)
            sql_select = 'SELECT * FROM nar WHERE 開催日 = ? AND 馬名 = ?' # 旧データの抽出の型。開催日と馬名で一意の行を指定。(%sは、%でエラー出る?)
            data_1 = (new_row[1], new_row[9]) # 上記の型に渡すデータ

            old_row = cur.execute(sql_select, data_1) # 旧データの指定行を抽出
            # <sqlite3.Cursor object at 0x1248f5dc0>
            old_row = old_row.fetchall() # 旧データの値を取得

            # old_row = cur.execute('SELECT * FROM nar WHERE 開催日 = %s AND 馬名 = %s'), (new_row[1], new_row[9]);


            if old_row == []: # old_rowが空のリストかどうか判断
                sql_insert = 'INSERT INTO nar ([開催日],[開催場所],[レース],[着順],[枠],[馬番],[逆番],[印],[馬名],[騎手],[厩舎],[単勝オッズ],[人気]) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
                data_2 = (
                    new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6],
                    new_row[7], new_row[8], new_row[9], new_row[10], new_row[11], new_row[12], new_row[13]
                    ) # 上記の型に渡すデータ
                print('インサート', data_2)
                cur.execute(sql_insert, data_2)

                # cur.execute('INSERT INTO nar ([開催日],[開催場所],[レース],[着順],[枠],[馬番],[逆番],[印],[馬名],[騎手],[厩舎],[単勝オッズ],[人気]) VALUES(new_row)')


            else: # すでにデータがあれば比較処理
                old_row = old_row[0] # リスト内タプルから、リスト解除

                if not data_comparator.compare_data(new_row, old_row): # データに差異があるか判断
                    # print(old_row,'old', '\n',new_row,'new')

                    # 差異ありならアップデート処理
                    sql_update = 'UPDATE nar SET 着順 = ?, 印 = ?, 騎手 = ?, 単勝オッズ = ?, 人気 = ?  WHERE 開催日 = ? AND 馬名 = ?'
                    data_3 = (new_row[4], new_row[8], new_row[10], new_row[12], new_row[13],   new_row[1], new_row[9])
                    print('アップデート', data_3, '\n')

                    cur.execute(sql_update, data_3)
                else:
                    print('スルー', '\n')
                    pass
                
        conn.commit()
        conn.close()



if __name__ == '__main__':
    a = RaceInfoAnalyzer('川崎競馬場')
    a.scraping_shutuba_table(2021, 10, 11, 9)
    a.scraping_race_result()
    a.save_db()
