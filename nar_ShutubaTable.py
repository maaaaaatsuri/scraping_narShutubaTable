#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# ----------競馬場コードを格納する辞書を作る。key=場名、value=場コードNo.-----------
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

    
#　場コードの多重リストの解消
def flatten_2d(data):
    for block in data:
        for elem in block:
            yield elem
jyo_cd = list(flatten_2d(jyo_cd))


# jyo_cdリスト をint型に変換
jyo_cd_int = [int(i) for i in jyo_cd]


# dict{場名: 場コード}が一旦完成
jyo_dict = dict(zip(jyo_text, jyo_cd_int))
# -------------------------------------------------------------------------


# -------------------------出馬表スクレイピング部分----------------------------
# 競馬場名を入力して、jyo_cdを取得(仮)
s_jyo_code = jyo_dict['門別競馬場']

# 出馬表スクレイピングクラス(仮)
class RaceInfoAnalyzer():
    def __init__(self):
        self.shutuba_table = pd.DataFrame()

    # 出馬表スクレイピング関数(仮)、引数に"年"、"s_jyoCode"、"月"、"日"、"レースナンバー"を入力
    def scraping_shutuba_table(self, year, s_jyo_code, month, day, race_num):
        
        # 引数からレースIDを作成
        race_id = str(year) + str(s_jyo_code).zfill(2) + str(month).zfill(2) + str(day).zfill(2) + str(race_num).zfill(2)
        race_id = int(race_id)
        
        # 指定レースから最終レースまでのレースIDをリストに格納
        race_id_lst = []
        race_counts = race_num
        i = 0
        while race_counts <= 12:
            race_id_lst.append(str(race_id))
            race_id += 1
            race_counts += 1

        # 出馬表自動取得
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

        print(self.shutuba_table, '\n'*3)
        browser.quit()
# -------------------------------------------------------------------------


# -------------------------データ成型部分(仮)---------------------------------

    def molding_data(self):

        # 不要列削除、カラム名変更
        self.shutuba_table = self.shutuba_table[[0, 1, 3, 6, 7, 9]]
        self.table_new = self.shutuba_table.set_axis(['枠番','馬番','馬名','騎手','厩舎','オッズ'], axis='columns')

        # rowName(レースID)をレースNo.に表示変更(要改良)
        table_new = self.table_new.rename(index={
            '202130090801':'1R', '202130090802':'2R',
            '202130090803':'3R', '202130090804':'4R',
            '202130090805':'5R', '202130090806':'6R',
            '202130090807':'7R', '202130090808':'8R',
            '202130090809':'9R', '202130090810':'10R',
            '202130090811':'11R', '202130090812':'12R',
        })

        #騎手列抽出
        self.jockey_lst = table_new.loc[::, '騎手']

        # 重複削除
        self.jockey_lst = self.jockey_lst.drop_duplicates()
# -------------------------------------------------------------------------


# -----------------------------データ出力部分(仮)-----------------------------
    def output(self):

        # 騎手ごとのレース情報
        for j in self.jockey_lst:
            k = self.table_new.query('騎手 == "{}"'.format(j))
            print(k,'\n'*2)
# -------------------------------------------------------------------------


# やりたいこと：レース情報を出力したい
test = RaceInfoAnalyzer()
# スクレイピング
test.scraping_shutuba_table(2021, s_jyo_code, 9, 8, 10)
# データ成形
test.molding_data()
# データ出力
test.output()













