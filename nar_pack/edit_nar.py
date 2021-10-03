from numpy import integer
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from python_utils.utils import Utils
from molding_data import MoldingNarData

import time
import datetime
import  sqlite3


pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.max_columns', 25)
pd.set_option('display.max_rows', 40)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.unicode.east_asian_width', True)


# レース情報分析クラス
class RaceInfoAnalyzer():
    def __init__(self, jyo_name):
        self.shutuba_table = pd.DataFrame()
        jyo_dict = MoldingNarData.make_jyo_dict(self)
        time.sleep(2)
        self.selected_code = jyo_dict[jyo_name]

# =======================================出馬表スクレイピング========================================================
    # 出馬表スクレイピング関数、引数に("年"、"selected_code"、"月"、"日"、"レースナンバー")を入力
    def scraping_shutuba_table(self, year, month, day, race_num):
        
        self.date = str(year) + str('-') + str(month).zfill(2) + str('-') + str(day).zfill(2)
        self.date = datetime.datetime.strptime(self.date, "%Y-%m-%d")
        race_id = str(year) + str(self.selected_code).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(race_num).zfill(2)
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
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=' + str(race_id)
            self.browser.get(url)
            elems = self.browser.find_elements_by_class_name('HorseList')
            for elem in elems:
                tds = elem.find_elements_by_tag_name('td')
                row = []
                for td in tds:
                    row.append(td.text)
                self.shutuba_table = self.shutuba_table.append(pd.Series(row, name=race_id))
        self.shutuba_table.columns = ['枠','馬番','印','馬名','性齢','斤量','騎手','厩舎','馬体重(増減)','単勝オッズ','人気','','']

        # 逆番カラム追加コード
        indiv_rev_num = []
        all_rev_num = []
        temp = 1
        for value in self.shutuba_table.index:
            while value:
                if temp == 1 or value == previous_value:
                    indiv_rev_num.append(temp)
                    temp += 1
                elif value != previous_value:
                    temp = 1
                    all_rev_num.append(indiv_rev_num[::-1])
                    indiv_rev_num.clear()
                    indiv_rev_num.append(temp)
                    temp += 1

                previous_value = value
                value = False
        all_rev_num.append(indiv_rev_num[::-1])
        all_rev_num = list(Utils.flatten_2d(all_rev_num))
        self.shutuba_table['逆番'] = all_rev_num

#         逆番カラム追加コード
#         MoldingNarData.add_reverse_column(self, self.shutuba_table)
#         print(self.shutuba_table)

        
        # 行名からレース番号カラム作成、追加
        i_lst = []
        for i in self.shutuba_table.index:
            i_lst.append(str(i)[-2:])
        self.shutuba_table.index = i_lst

        self.shutuba_table = self.shutuba_table.rename(index={
            '01': '1R', '02': '2R',
            '03': '3R', '04': '4R',
            '05': '5R', '06': '6R',
            '07': '7R', '08': '8R',
            '09': '9R', '10': '10R',
            '11': '11R', '12': '12R'})
        
        self.shutuba_table['開催日'] = self.date
        self.shutuba_table['レース'] = self.shutuba_table.index
        self.shutuba_table['着順'] = '--'
        
        self.shutuba_table = self.shutuba_table[['開催日','レース','着順','枠','馬番','逆番','印','馬名','騎手','厩舎','単勝オッズ','人気']]
        print('='*5,'【 出 馬 表 】','='*85, '\n', self.shutuba_table)
        return self.shutuba_table
        
# =====================================レース結果スクレイピング========================================================
    # 着順を取得
    def scraping_race_result(self):
        self.race_result = self.shutuba_table
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/result.html?race_id=' + str(race_id)
            self.browser.get(url)

            horse_Names = self.browser.find_elements_by_class_name("Horse_Name")
            h_ls = [h.text for h in horse_Names if h.text != '馬名']

            ranks = self.browser.find_elements_by_class_name("Rank")
            r_ls = [r.text for r in ranks]

            rh_dict = dict(zip(h_ls, r_ls))
            
            for k in rh_dict.keys():
                i=0
                while k != self.race_result['馬名'][i]:
                    i+=1
                self.race_result['着順'][i] = rh_dict[k]
        print('='*5,'【 レ ー ス 結 果 】','='*80, '\n', self.race_result)

        self.browser.quit()
        return self.race_result



# =====================================DB作成========================================================
    def make_db(self):
        
        db_name = 'nar_nagoya.db'
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()


        self.race_result.to_sql(
            'nar_nagoya', conn, if_exists='replace', index=None
            )


        # cur.execute('INSERT INTO persons(name) values("Taro")')
        # cur.execute('SELECT * FROM persons')
        # print(cur.fetchall())



        conn.commit()
        conn.close()




if __name__ == '__main__':
    nagoya = RaceInfoAnalyzer('名古屋競馬場')
    nagoya.scraping_shutuba_table(2021, 10, 1, 12)
    nagoya.scraping_race_result()
    nagoya.make_db()

