#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from python_utils.utils import Utils

options = Options()
options.add_argument('--headless')
pd.set_option('display.unicode.east_asian_width', True)


# =========================競馬場コードを格納する辞書を作る。key=場名、value=場コードNo.===================================
url = "https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu"
response = req.urlopen(url)
parse_html = BeautifulSoup(response, "html.parser")

tags_a = parse_html.find_all('a')

jyo_text = []
jyo_cd = []
# 手動で対象タグのindex番号を指定しているため要改良
for a in tags_a[21:36]:
    text = a.text
    href = a.attrs['href']
    href = re.findall("[0-9]+", str(href))
    jyo_text.append(text.replace('\n', ''))
    jyo_cd.append(href)

jyo_cd = list(Utils.flatten_2d(jyo_cd))

jyo_cd_int = [int(i) for i in jyo_cd]
jyo_dict = dict(zip(jyo_text, jyo_cd_int))
# ==============================================================================================================
# =======================================出馬表スクレイピング部分=====================================================
selected_code = jyo_dict['大井競馬場']

# レース情報分析クラス
class RaceInfoAnalyzer():
    def __init__(self):
        self.shutuba_table = pd.DataFrame()

    # 出馬表スクレイピング関数、引数に("年"、"selected_code"、"月"、"日"、"レースナンバー")を入力
    def scraping_shutuba_table(self, year, selected_code, month, day, race_num):
        race_id = str(year) + str(selected_code).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(race_num).zfill(2)
        race_id = int(race_id)
        
        self.race_id_lst = []
        race_counts = race_num
        while race_counts <= 12:
            self.race_id_lst.append(race_id)
            race_id += 1
            race_counts += 1
            
        # 出馬表を取得
        self.shutuba_table = pd.DataFrame()
        browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=' + str(race_id)
            browser.get(url)
            elems = browser.find_elements_by_class_name('HorseList')
            for elem in elems:
                tds = elem.find_elements_by_tag_name('td')
                row = []
                for td in tds:
                    row.append(td.text)
                self.shutuba_table = self.shutuba_table.append(pd.Series(row, name=race_id))
        browser.quit()
                
        # 全てのカラム名を変更
        self.shutuba_table.columns = ['枠','馬番','印','馬名','性齢','斤量','騎手','厩舎','馬体重(増減)','単勝オッズ','人気','','']
# ===============================================================================================================
# ========================================レース結果スクレイピング部分==================================================
    def scraping_race_result(self):
        
        # レース結果を取得
        self.result_all = pd.DataFrame()
        for race_id in self.race_id_lst:
            url = 'https://nar.netkeiba.com/race/result.html?race_id=' + str(race_id)
            try:
                table = pd.read_html(url)
            except ValueError as e:
                print('catch ValueError:',e, '(※ まだ行われていないレースがあります。)')
            else:
                race_result = table[0]
                self.result_all = self.result_all.append(race_result)

        index_lst = []
        race_id_i = 0
        index_i = 0
        count = 0
        for i in self.result_all.index:
            
            if count == 0 or self.result_all.index[index_i] > self.result_all.index[index_i-1]:
                index_lst.append(self.race_id_lst[race_id_i])
                count += 1
            else:
                index_lst.append(self.race_id_lst[race_id_i+1])
                race_id_i += 1
            index_i += 1

        self.result_all['index'] = index_lst
        self.result_all.set_index = self.result_all.set_index('index', inplace=True)
        self.result_all.index.name = None
# ===============================================================================================================
# ========================================出馬表成型部分===========================================================
    def molding_table(self):
        self.clipping_table = self.shutuba_table
        
        indiv_rev_num = []
        all_rev_num = []
        temp = 1
        for value in self.clipping_table.index:
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
        self.clipping_table['逆番'] = all_rev_num
        self.clipping_table = self.clipping_table[['枠','馬番','逆番','印','馬名','騎手','厩舎','単勝オッズ','人気']]
        

        i_lst = []
        for i in self.clipping_table.index:
            i_lst.append(str(i)[-2:])
        self.clipping_table.index = i_lst

        self.clipping_table = self.clipping_table.rename(index={
            '01': '1R', '02': '2R',
            '03': '3R', '04': '4R',
            '05': '5R', '06': '6R',
            '07': '7R', '08': '8R',
            '09': '9R', '10': '10R',
            '11': '11R', '12': '12R'})
        
        print('\n'*1, '★-'*10,'出 馬 表', '★-'*10, '\n'*1)
        print(self.clipping_table)
# ================================================================================================================
# =========================================レース結果成型部分=========================================================
    def molding_result(self):

        i_lst = []
        for i in self.result_all.index:
            i_lst.append(str(i)[-2:])
        self.result_all.index = i_lst

        self.result_all = self.result_all.rename(index={
            '01': '1R', '02': '2R',
            '03': '3R', '04': '4R',
            '05': '5R', '06': '6R',
            '07': '7R', '08': '8R',
            '09': '9R', '10': '10R',
            '11': '11R', '12': '12R'})
        self.disposing_table = self.result_all[['着順','枠','馬番','馬名','騎手','厩舎','単勝オッズ','人気']]
        self.disposing_table.fillna(0)
        self.disposing_table.astype(int, errors='ignore')
# ===============================================================================================================
# =========================================出馬表とレース結果マージ部分================================================
    def merge_data(self):

        self.disposing_table['index'] = self.disposing_table.index
        self.merge_data = pd.merge(self.clipping_table, self.disposing_table, on='馬名', suffixes=['', '_重複'])
        
        self.merge_data.set_index = self.merge_data.set_index('index', inplace=True)
        self.merge_data.index.name = None

        self.merge_data = self.merge_data[['着順','枠','馬番','逆番','印','馬名','騎手','厩舎','単勝オッズ','人気']]

        print('\n'*1, '★-'*10,'レ ー ス 結 果', '★-'*10, '\n'*1)
        print(self.merge_data)
# ===============================================================================================================
# =======================================データ出力部分(騎手テーブル)=================================================
    def output_jocky_table(self):
        
        jockey_lst = self.clipping_table.loc[::, '騎手']
        jockey_lst = jockey_lst.drop_duplicates()
        
        
        # 騎手ごとのレース情報を出力
        print('\n'*1, '★-'*10,'騎 手 テ ー ブ ル','★-'*10, '\n'*1)
        for j in jockey_lst:
            focus_jockey_table = self.clipping_table.query('騎手 == "{}"'.format(j))
            print(focus_jockey_table, '\n'*1)
            
        # 騎手ごとのレース結果を出力
        print('\n'*1, '★-'*10,'騎 手 テ ー ブ ル (結果)','★-'*10, '\n'*1)
        for j in jockey_lst:
            focus_jockey_result = self.merge_data.query('騎手 == "{}"'.format(j))
            print(focus_jockey_result, '\n'*1)
# ===============================================================================================================
# =======================================データ出力部分(厩舎テーブル)=================================================
    def output_stable_table(self):
        
        stable_lst = self.clipping_table.loc[::, '厩舎']
        stable_lst = stable_lst.drop_duplicates()
        
        
        # 厩舎ごとのレース情報を出力
        print('\n'*1, '★-'*10,'厩 舎 テ ー ブ ル','★-'*10, '\n'*1)
        for s in stable_lst:
            focus_stable_table = self.clipping_table.query('厩舎 == "{}"'.format(s))
            print(focus_stable_table, '\n'*1)

        # 厩舎ごとのレース情報を出力
        print('\n'*1, '★-'*10,'厩 舎 テ ー ブ ル (結果)','★-'*10, '\n'*1)
        for s in stable_lst:
            focus_stable_table = self.merge_data.query('厩舎 == "{}"'.format(s))
            print(focus_stable_table, '\n'*1)            
# ===============================================================================================================



if __name__ == '__main__':
    test = RaceInfoAnalyzer()
    test.scraping_shutuba_table(2021, selected_code, 9, 18, 1)
    test.scraping_race_result()
    test.molding_table()
    test.molding_result()
    test.merge_data()
    test.output_jocky_table()
#     test.output_stable_table()





