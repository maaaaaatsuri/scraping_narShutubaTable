#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# ----------競馬場コードを格納する辞書を作る。key=場名、value=場コードNo.------------
url = "https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu"
response = req.urlopen(url)
parse_html = BeautifulSoup(response, "html.parser")

# aタグ-textから場名、-href属性から場コード を抽出
tags_a = parse_html.find_all('a')

jyo_text = []
jyo_cd = []
# 手動でタグのindexを指定しているため要改良
for a in tags_a[21:36]:
    text = a.text

    href = a.attrs['href']
    href = re.findall("[0-9]+", str(href))

    jyo_text.append(text.replace('\n', ''))
    jyo_cd.append(href)

    
#　場コードの多重リストを解消
def flatten_2d(data):
    for block in data:
        for elem in block:
            yield elem
jyo_cd = list(flatten_2d(jyo_cd))

# jyo_cd をint型に変換
jyo_cd_int = [int(i) for i in jyo_cd]

# dict{場名: 場コード}が一旦完成
jyo_dict = dict(zip(jyo_text, jyo_cd_int))
# -------------------------------------------------------------------------

# -------------------------出馬表スクレイピング部分----------------------------
# 競馬場名を入力して、jyo_cdを取得(仮)
selected_code = jyo_dict['大井競馬場']

# レース情報分析クラス
class RaceInfoAnalyzer():
    def __init__(self):
        self.shutuba_table = pd.DataFrame()

    # 出馬表スクレイピング関数、引数に("年"、"selected_code"、"月"、"日"、"レースナンバー")を入力
    def scraping_shutuba_table(self, year, selected_code, month, day, race_num):
        
        # 引数からレースIDを作成
        race_id = str(year) + str(selected_code).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(race_num).zfill(2)
        race_id = int(race_id)
        
        # 指定レースから最終レースまでのレースIDをリストに格納
        race_id_lst = []
        race_counts = race_num
        while race_counts <= 12:
            race_id_lst.append(race_id)
            race_id += 1
            race_counts += 1
            
        # 出馬表を取得
        self.shutuba_table = pd.DataFrame()
        browser = webdriver.Chrome(ChromeDriverManager().install())
        for race_id in race_id_lst:
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
# -------------------------------------------------------------------------

# -------------------------データ成型部分(仮)---------------------------------
    def molding_data(self):

        # 不要列削除、全てのカラム名を変更(set.axis)
        self.clipping_table = self.shutuba_table.drop([2, 4, 5, 8, 10, 11, 12], axis=1)
        self.clipping_table = self.clipping_table.set_axis(['枠番','馬番','馬名','騎手','厩舎','オッズ'], axis=1)

        # 裏馬番カラムの追加と並び替え
        self.clipping_table = self.clipping_table.reindex(['枠番','馬番','裏馬番','馬名','騎手','厩舎','オッズ'], axis=1)
        
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


        #　all_rev_numの多重リストの解消
        def flatten_2d(data):
            for block in data:
                for elem in block:
                    yield elem
        all_rev_num = list(flatten_2d(all_rev_num))
        self.clipping_table['裏馬番'] = all_rev_num

        print(self.clipping_table)
        
        
        # row_name(レースID)をレースNo.に表示変更(要改良)
        # self.clipping_table = self.clipping_table.rename(index={
        #     '202130090801':'1R', '202130090802':'2R',
        #     '202130090803':'3R', '202130090804':'4R',
        #     '202130090805':'5R', '202130090806':'6R',
        #     '202130090807':'7R', '202130090808':'8R',
        #     '202130090809':'9R', '202130090810':'10R',
        #     '202130090811':'11R', '202130090812':'12R',
        # })

        # 騎手列抽出
        self.jockey_lst = self.clipping_table.loc[::, '騎手']

        # 重複削除
        self.jockey_lst = self.jockey_lst.drop_duplicates()
# -------------------------------------------------------------------------

# ---------------------------データ出力部分(仮)-------------------------------
    def output(self):

        # 騎手ごとのレース情報を出力
        for j in self.jockey_lst:
            focus_jockey_table = self.clipping_table.query('騎手 == "{}"'.format(j))
            print(focus_jockey_table,'\n'*2)
# -------------------------------------------------------------------------

# やりたいこと：レース情報を出力したい
test = RaceInfoAnalyzer()
# スクレイピング
test.scraping_shutuba_table(2021, selected_code, 9, 10, 1)
# データ成形
test.molding_data()
# データ出力
test.output()




