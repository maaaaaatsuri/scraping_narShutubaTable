#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


# ---競馬場コードを格納する辞書を作るため、keyとして場名、valueとして場コードNo.を抽出する---

url = "https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu"
response = req.urlopen(url)
parse_html = BeautifulSoup(response, "html.parser")

# aタグ-textから場名、-href属性から場コード を抽出
tags_a = parse_html.find_all('a')
# print(tags_a)
# print(tags_a[21:36])＊＊要改良＊＊

jyo_text = []
jyo_cd = []
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
# print(jyo_text)
# print(jyo_cd)


# jyo_cdリスト をint型に変換
jyo_cd_int = [int(i) for i in jyo_cd]


# dict{場名: 場コード}が一旦完成
jyo_dict = dict(zip(jyo_text, jyo_cd_int))
# print(jyo_dict)

# ----------------------------------------------------------------------------



# --------------------------出馬表スクレイピング部分------------------------------

# 競馬場名を入力して、jyo_cdを取得(仮)
s_jyoCode = jyo_dict['門別競馬場']

# レース情報分析クラス
class RaceInfoAnalyzer():
    
    def __init__(self):
        self.shutuba_table = pd.DataFrame()

    # 出馬表スクレイピング関数(仮)、引数に"年"、"s_jyoCode"、"月"、"日"、"レースナンバー"を入力
    def scrape_shutuba_table(self, year, s_jyoCode, month, day, raceNum):
        # インスタンス変数にする必要なし
        self.year = year
        self.s_jyoCode = s_jyoCode
        self.month = month
        self.day = day
        self.raceNum = raceNum
        
        # 引数からレースIDを作成
        raceId = str(self.year) + str(self.s_jyoCode).zfill(2) + str(self.month).zfill(2) + str(self.day).zfill(2) + str(self.raceNum).zfill(2)
        raceId = int(raceId)
        
        # 指定レースから最終レースまでのレースIDをリストに格納
        raceId_lst = []
        race_counts = self.raceNum
        i = 0
        while race_counts <= 12:
            raceId_lst.append(str(raceId))
            raceId += 1
            race_counts += 1
        # print(raceId_lst)

        # 出馬表自動取得
        self.shutuba_table = pd.DataFrame()
        browser = webdriver.Chrome(ChromeDriverManager().install())
        for raceId in raceId_lst:
            url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=' + str(raceId)
            browser.get(url)
            elements = browser.find_elements_by_class_name('HorseList')
            
            for element in elements:
                tds = element.find_elements_by_tag_name('td')
                row = []
                for td in tds:
                    row.append(td.text)
                self.shutuba_table = self.shutuba_table.append(pd.Series(row, name=raceId))

        print(self.shutuba_table, '\n'*4)
        browser.quit()

    def molding_data(self):
        # table.columns

        # 不要列削除、カラム名変更
        self.shutuba_table = self.shutuba_table[[0, 1, 3, 6, 7, 9]]
        self.table_new = self.shutuba_table.set_axis(['枠番','馬番','馬名','騎手','厩舎','オッズ'], axis='columns')
        # table_new

        # table_new.dtypes
        # table_new.index
        # Index(['202130083101', '202130083101', '202130083101', '202130083101',
        #        '202130083101', '202130083101', '202130083101', '202130083101',
        #        '202130083102', '202130083102',
        #        ...
        #        '202130083112', '202130083112', '202130083112', '202130083112',
        #        '202130083112', '202130083112', '202130083112', '202130083112',
        #        '202130083112', '202130083112'],
        #       dtype='object', length=118)


        # rowName(レースID)をレースNo.に表示変更
        self.table_new = self.table_new.rename(index={
            '202130090801':'1R', '202130090802':'2R',
            '202130090803':'3R', '202130090804':'4R',
            '202130090805':'5R', '202130090806':'6R',
            '202130090807':'7R', '202130090808':'8R',
            '202130090809':'9R', '202130090810':'10R',
            '202130090811':'11R', '202130090812':'12R',
        })
        # print(table_new)


        #騎手列抽出
        self.Jockey_lst = self.table_new.loc[::, '騎手']

        # 重複削除
        self.Jockey_lst = self.Jockey_lst.drop_duplicates()

    def output(self):
        # 騎手ごとのレース情報
        for j in self.Jockey_lst:
            k = self.table_new.query('騎手 == "{}"'.format(j))
            print(k,'\n'*2)

# ---------------------------ここまでが関数内---------------------------------

# やりたいこと：レース情報を出力したい
test = RaceInfoAnalyzer()

# スクレイピングしてー
test.scrape_shutuba_table(2021, s_jyoCode, 9, 8, 10)

# 成形してー
test.molding_data()

# 出力
test.output()











