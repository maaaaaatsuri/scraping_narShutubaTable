import urllib.request as req
from bs4 import BeautifulSoup
import re
from python_utils.utils import Utils

from typing import *
import pandas as pd


class MoldingNarData():
    
    # 競馬場コードを格納する辞書を作る。{例 -> '帯広競馬場': 65, ...}
    def make_jyo_dict(self):
        url = "https://nar.netkeiba.com/racecourse/racecourse_list.html?rf=sidemenu"
        response = req.urlopen(url)
        parse_html = BeautifulSoup(response, "html.parser")

        tags_a = parse_html.find_all('a')

        jyo_text = []
        jyo_cd = []
        for a in tags_a[21:36]:
            text = a.text
            href = a.attrs['href']
            href = re.findall("[0-9]+", str(href))
            jyo_text.append(text.replace('\n', ''))
            jyo_cd.append(href)

        jyo_cd = list(Utils.flatten_2d(jyo_cd))

        jyo_cd_int = [int(i) for i in jyo_cd]
        jyo_dict = dict(zip(jyo_text, jyo_cd_int))
        return jyo_dict

    # if __name__ == "__main__":
    # a = Make_jyo_dict()
    # jyo_dict = a.make_jyo_dict()
    # print(sys.path)

    
        
    # 逆番カラム追加コード
    def add_reverse_column(self, data):
        indiv_rev_num = []
        all_rev_num = []
        temp = 1
        for value in data.index:
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
        data['逆番'] = all_rev_num
        return data



# (self, data: pd.DataFrame) ->  pd.DataFrame:
