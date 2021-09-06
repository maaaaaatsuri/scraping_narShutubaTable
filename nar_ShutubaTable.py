#!/usr/bin/env python
# coding: utf-8

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import urllib.request as req
import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
-----------------出馬表スクレイピング部分----------------------
"""

# 指定開催場の一日のレースID取得(手動で変数を設定)
raceNum = 202130083101  # ある日の第1レースのレースID
race_counts = 1
last_raceNum = 12

raceNums = []
while race_counts <= last_raceNum:
    raceNums.append(str(raceNum))
    raceNum += 1
    race_counts += 1

# 出馬表自動取得コード
table = pd.DataFrame()
browser = webdriver.Chrome(ChromeDriverManager().install())
for raceNum in raceNums:
    url = 'https://nar.netkeiba.com/race/shutuba.html?race_id=' + raceNum
    browser.get(url)
    HorseLists = browser.find_elements_by_class_name('HorseList')
    for HorseList in HorseLists:
        tds = HorseList.find_elements_by_tag_name('td')
        row = []
        for td in tds:
            row.append(td.text)
        table = table.append(pd.Series(row, name=raceNum))

print(table)
browser.quit()


# table.columns

# 不要列削除、カラム名変更
table = table[[0, 1, 3, 6, 7, 9]]
table_new = table.set_axis(['枠番','馬番','馬名','騎手','厩舎','オッズ'], axis='columns')
table_new

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
table_new = table_new.rename(index={
    '202130083101':'1R', '202130083102':'2R',
    '202130083103':'3R', '202130083104':'4R',
    '202130083105':'5R', '202130083106':'6R',
    '202130083107':'7R', '202130083108':'8R',
    '202130083109':'9R', '202130083110':'10R',
    '202130083111':'11R', '202130083112':'12R',
})

print(table_new)


#騎手列抽出
Jockey_lst = table_new.loc[::, '騎手']
Jockey_lst

# 重複削除
Jockey_lst = Jockey_lst.drop_duplicates()
Jockey_lst


# 騎手名リスト作成、
jockey_name = []
for j in Jockey_lst:
    jockey_name.append(j)
# print(jockey_name)

# 騎手ごとのレース情報
for j in Jockey_lst:
    k = table_new.query('騎手 == "{}"'.format(j))
    print(k,'\n'*2)

""""
--------------ここまで----------------
"""
