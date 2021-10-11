import pandas as pd
from selenium import webdriver
import time
import datetime


df5 = pd.DataFrame(data={
        '列1': pd.Series([10, 20, 30, 40, 50, 60, 70], 
                          index=['行1','行2','行3','行4','行5','行6','行7']), 
        '列2': pd.Series([100, 200, 300, 400, 500, 600, 700], 
                          index=['行1','行2','行3','行4','行5','行6','行7']),
        '列3': pd.Series(['b', 'c', 'd', 'e', 'r', 't', 'y'], 
                          index=['行1','行2','行3','行4','行5','行6','行7'])}
        )

# print(df5, '\n'*2)


# # for t in df5.itertuples(name=None):
# l = []
# for t in df5.itertuples(name=None):
#     print(t)
#     l.append(t)

# print(l)



date_a = str(2021) + str('/') + str(10).zfill(2) + str('/') + str(1).zfill(2)
print(date_a, type(date_a))
date_a = str(datetime.datetime.strptime(date_a, "%Y/%m/%d"))
print(date_a, type(date_a))


















# s = pd.Series(['b', 'c', 'd', 'e', 'r', 't', 'y'], index=['行1','行2','行3','行4','行5','行6','行7'])
# s = pd.DataFrame(s)
# print(s.T)

# browser = webdriver.Safari()
# browser.get('https://mainichi.jp/')
# time.sleep(3)
# browser.quit()

