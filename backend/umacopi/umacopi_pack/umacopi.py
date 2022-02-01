from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from utils import Utils

from date_creator import DateCreator

from venue_code_creator import VenueCodeCreator
from reverse_number_adder import ReverseNumberAdder
from race_number_adder import RaceNumberAdder
from data_comparator import DataComparator
from type_changer import TypeChanger
import pandas as pd
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
        # self.browser = webdriver.Chrome(ChromeDriverManager().install())
        options = Options()
        options.add_argument('--headless')
        options.add_argument('no-sandbox')
        self.browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)
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

        columns_name_list = ['frame','umaban','mark','horse_name','age','weight','jockey','stable','horse_weight(fluctuated)','odds','popularity','','']
        combined_columns = [columns_name_list[0:len(self.shutuba_table.columns + 1)]]
        combined_columns = list(Utils.flatten_2d(combined_columns))
        
        self.shutuba_table.columns = [x for x in combined_columns]

        # 開催日カラム追加
        self.shutuba_table['held_date'] = self.date

        # 開催場所カラム追加
        venue_dict_swap = {v: k for k, v in self.venue_dict.items()}
        self.shutuba_table['venue'] = venue_dict_swap[self.selected_venue]

        # レース(番号)カラム追加
        race_number_adder = RaceNumberAdder()
        self.shutuba_table = race_number_adder.add_race_number(self.shutuba_table)

        # 着順(空値)カラム追加
        self.shutuba_table['rank'] = '--'

        # 逆番カラム追加
        reverse_number_adder = ReverseNumberAdder()
        self.shutuba_table = reverse_number_adder.add_reverse_number(self.shutuba_table)

        # 対象カラムのデータ型をDBに合わせて変換
        self.shutuba_table['frame'] = self.type_changer.change_to_int(self.shutuba_table['frame'])
        self.shutuba_table['umaban'] = self.type_changer.change_to_int(self.shutuba_table['umaban'])
        self.shutuba_table['popularity'] = self.type_changer.change_to_int(self.shutuba_table['popularity'])
        self.shutuba_table['odds'] = self.type_changer.change_to_float(self.shutuba_table['odds'])

        self.shutuba_table = self.shutuba_table[[
            'held_date','venue','race_number','rank','frame','umaban','rev_umaban',
            'mark','horse_name','jockey','stable','odds','popularity'
            ]]
        self.shutuba_table = self.shutuba_table.reset_index(drop=True)
        # print('='*5,'【 出 馬 表 】','='*85, '\n', self.shutuba_table)
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
                while k != self.shutuba_table['horse_name'][i]:
                    i += 1
                self.shutuba_table['rank'][i] = self.type_changer.result_int(name_rank_dict[k])
        print('='*5,'【 レ ー ス 結 果 】','='*80, '\n', self.shutuba_table, '\n')

        self.browser.quit()
        return self.shutuba_table
# ===============================================DBに保存============================================================
    # def save_db(self):
    #     db_name = '/root/HorseRacingAnalyzer/web/db.sqlite3'
    #     conn = sqlite3.connect(db_name)
    #     cur = conn.cursor()

    #     data_comparator = DataComparator()
    #     for new_row in self.shutuba_table.itertuples(name=None):
    #         sql_select = 'SELECT * FROM umacopi_narmodel WHERE held_date = ? AND horse_name = ?'
    #         unique_key = (new_row[1], new_row[9])

    #         old_row = cur.execute(sql_select, unique_key)
    #         old_row = old_row.fetchall()

    #         if old_row == []:
    #             sql_insert = 'INSERT INTO umacopi_narmodel ([held_date],[venue],[race_number],[rank],[frame],[umaban],[rev_umaban],[mark],[horse_name],[jockey],[stable],[odds],[popularity]) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)'
    #             new_row_data = (
    #                 new_row[1], new_row[2], new_row[3], new_row[4], new_row[5], new_row[6],
    #                 new_row[7], new_row[8], new_row[9], new_row[10], new_row[11], new_row[12], new_row[13]
    #                 )
    #             cur.execute(sql_insert, new_row_data)
    #             temp_counts = 0
    #         else:
    #             old_row = old_row[0]
    #             if not data_comparator.compare_data(new_row, old_row):
    #                 sql_update = 'UPDATE umacopi_narmodel SET rank = ?, mark = ?, jockey = ?, odds = ?, popularity = ?  WHERE held_date = ? AND horse_name = ?'
    #                 update_data = (new_row[4], new_row[8], new_row[10], new_row[12], new_row[13],   new_row[1], new_row[9])
    #                 cur.execute(sql_update, update_data)
    #                 temp_counts = 1
    #             else:
    #                 temp_counts = 2
    #                 pass

    #     if temp_counts == 0:
    #         print('※ 新規データを追加しました。', '\n')
    #     elif temp_counts == 1:
    #         print('※ データを更新しました。', '\n')
    #     else:
    #         print('※ 更新はありません。', '\n')

    #     conn.commit()
    #     conn.close()


# if __name__ == '__main__':
#     args = sys.argv
#     copi_nar = RaceInfoAnalyzer(args[1])
#     copi_nar.scraping_shutuba_table(args[2], args[3], args[4], int(args[5]))
#     copi_nar.scraping_race_result()
#     copi_nar.save_db()



# ================================================DB処理を管理=======================================================
class DbManager(RaceInfoAnalyzer):

    def __init__(self, dbname, venue, year, month, day, race_num):
        self.dbname = dbname
        date_creator = DateCreator()
        self.date = date_creator.create_date(year, month, day)
        ins = RaceInfoAnalyzer(venue)
        self.shutuba_table = ins.scraping_shutuba_table(year, month, day, race_num)
        self.shutuba_table = ins.scraping_race_result()

        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        # 開催場所、指定時の一回だけDB問い合わせ、データがなければINSERT実行
        sql_select_v = 'SELECT name FROM umacopi_mstvenue WHERE name = ?'
        v = cur.execute(sql_select_v, (venue,)) # 第二引数は要素一つでもタプルで記述(,)が必要
        v = v.fetchone()
        if v == None:
            sql_insert = 'INSERT INTO umacopi_mstvenue ([name]) VALUES(?)'
            cur.execute(sql_insert, (venue,))
        else:
            pass

        # レース情報、指定時の一回だけDB問い合わせ、データがなければINSERT実行
        print(self.date)
        select_raceinfo = 'SELECT date, venue_id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?'
        self.venue_id = cur.execute('SELECT id FROM umacopi_mstvenue WHERE name = ?', (venue,))
        self.venue_id = self.venue_id.fetchone()
        self.venue_id = self.venue_id[0]
        raceinfo = cur.execute(select_raceinfo, (self.date, self.venue_id))
        raceinfo = raceinfo.fetchone()
        if raceinfo == None:
            print('raceinfoインサートします')
            sql_insert = 'INSERT INTO umacopi_raceinfo ([date], [venue_id]) VALUES(?, ?)'
            cur.execute(sql_insert, (self.date, self.venue_id))
        else:
            print('raceinfoインサートはありません')
            pass

        conn.commit()
        cur.close()
        conn.close()


    def aaa(self):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()
        data_comparator = DataComparator()
        # select_path = 'sql_select.txt'
        # insert_path = 'sql_insert.txt'
        for new_row in self.shutuba_table.itertuples(name=None):
            # with open(select_path) as f:
            # for sql_select in f:
            # sql_select = sql_select.strip()

            sql_select_j = 'SELECT name FROM umacopi_mstjockey WHERE name = ?'
            j = cur.execute(sql_select_j, (new_row[10],)) # 第二引数は要素一つでもタプルで記述(,)が必要
            j = j.fetchone()
            sql_select_m = 'SELECT kind FROM umacopi_mstmark WHERE kind = ?'
            m = cur.execute(sql_select_m, (new_row[8],)) # 第二引数は要素一つでもタプルで記述(,)が必要
            m = m.fetchone()
            sql_select_s = 'SELECT name FROM umacopi_mststable WHERE name = ?'
            s = cur.execute(sql_select_s, (new_row[11],)) # 第二引数は要素一つでもタプルで記述(,)が必要
            s = s.fetchone()

            # print("jを表示", j, type(j))
            # print("mを表示", m, type(m))
            # print("sを表示", s, type(s))

            if j == None:
                print('jインサートします')
                sql_insert = 'INSERT INTO umacopi_mstjockey ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_row[10],))
            else:
                print('jインサートはありません')
                pass

            if m == None:
                print('mインサートします')
                sql_insert = 'INSERT INTO umacopi_mstmark ([kind]) VALUES(?)'
                cur.execute(sql_insert, (new_row[8],))
            else:
                print('mインサートはありません')
                pass

            if s == None:
                print('sインサートします')
                sql_insert = 'INSERT INTO umacopi_mststable ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_row[11],))
            else:
                print('sインサートはありません')
                pass
            print('\n')


# =============================       umacopi_racetable
            raceinfo = cur.execute('SELECT * FROM umacopi_raceinfo')
            raceinfo = raceinfo.fetchall()
            # print(raceinfo)

            # print(self.date)
            # print(self.venue_id)
            select_racetable = 'SELECT race_num, raceinfo_id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?'
            raceinfo_id = cur.execute('SELECT id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?', (self.date, self.venue_id))
            raceinfo_id = raceinfo_id.fetchone()
            # print(raceinfo_id)

            raceinfo_id = raceinfo_id[0]
            racetable = cur.execute(select_racetable, (new_row[3], raceinfo_id))
            racetable = racetable.fetchone()
            if racetable == None:
                print('racetableインサートします')
                sql_insert = 'INSERT INTO umacopi_racetable ([race_num], [raceinfo_id]) VALUES(?, ?)'
                cur.execute(sql_insert, (new_row[3], raceinfo_id))
            else:
                print('racetableインサートはありません')
                pass

    # =============================       umacopi_raceresults
            select_raceresults = 'SELECT umaban, racetable_id FROM umacopi_raceresults WHERE umaban = ? AND racetable_id = ?'
            racetable_id = cur.execute('SELECT id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?', (new_row[3], raceinfo_id))
            racetable_id = racetable_id.fetchone()
            # print(racetable_id)

            jockey_id = cur.execute('SELECT id FROM umacopi_mstjockey WHERE name = ?', (new_row[10],))
            jockey_id = jockey_id.fetchone()
            jockey_id = jockey_id[0]
            # print("jockey_id", jockey_id)
            
            mark_id = cur.execute('SELECT id FROM umacopi_mstmark WHERE kind = ?', (new_row[8],))
            mark_id = mark_id.fetchone()
            mark_id = mark_id[0]
            # print("mark_id", mark_id)

            stable_id = cur.execute('SELECT id FROM umacopi_mststable WHERE name = ?', (new_row[11],))
            stable_id = stable_id.fetchone()
            stable_id = stable_id[0]
            # print("stable_id", stable_id)

            racetable_id = racetable_id[0]
            raceresults = cur.execute(select_raceresults, (new_row[6], racetable_id))
            raceresults = raceresults.fetchone()
            if raceresults == None:
                print('raceresultsインサートします')
                sql_insert = 'INSERT INTO umacopi_raceresults ([rank],[frame],[umaban],[rev_umaban],[horse_name],[odds],[popularity],[jockey_id],[mark_id],[racetable_id],[stable_id]) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                cur.execute(sql_insert, (new_row[4], new_row[5], new_row[6], new_row[7], new_row[9], new_row[12], new_row[13], jockey_id, mark_id, racetable_id, stable_id))
            else:
                print('raceresultsインサートはありません')
                pass

# 作業用 (9, '2022/01/30', '佐賀競馬場', '11R', '--', 8, 10, 1, '--', 'オイカケマショウ', '長田進仁', '佐賀 中野博', 244.1, 10) 

        # raceinfo = cur.execute('SELECT * FROM umacopi_raceinfo')
        # raceinfo = raceinfo.fetchall()
        # print(raceinfo)
        # racetable = cur.execute('SELECT * FROM umacopi_racetable')
        # racetable = racetable.fetchall()
        # print(racetable)
        raceresults = cur.execute('SELECT * FROM umacopi_raceresults')
        raceresults = raceresults.fetchall()
        
        for r in raceresults:
            print(r)

        conn.commit()
        cur.close()
        conn.close()







        # j = cur.execute('SELECT * FROM umacopi_mstjockey')
        # j = j.fetchall()
        # m = cur.execute('SELECT * FROM umacopi_mstmark')
        # m = m.fetchall()
        # s = cur.execute('SELECT * FROM umacopi_mststable')
        # s = s.fetchall()


# def execute(self, sql_select):
# mstjockey_select = 'SELECT name FROM umacopi_mstjockey WHERE name = ?'
# mstmark_select = 'SELECT kind FROM umacopi_mstmark WHERE kind = ?'
# mststable_select = 'SELECT name FROM umacopi_mststable WHERE name = ?'
# mstvenue_select = 'SELECT name FROM umacopi_mstvenue WHERE name = ?'
# raceinfo_select = 'SELECT date, venue_id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?'
# racetable_select = 'SELECT race_num, raceinfo_id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?'
# raceresults_select = 'SELECT umaban, racetable_id FROM umacopi_raceresults WHERE umaban = ? AND racetable_id = ?'



    # with open(self.insert_path) as f:
    #     sql_insert = f.readline()
    #     def execute(self, sql_insert):
    #         conn = sqlite3.connect(self.dbname)
    #         cur = conn.cursor()
    #         cur.execute(sql_insert, insert_data)
    #         conn.commit()
    #         cur.close()
    #         conn.close()
    # print(mstjockey_insert, mstmark_insert)
    # print(mststable_insert, mstvenue_insert)
    # print(raceinfo_insert, racetable_insert)
    # print(raceresults_insert)


        # '''
        #     実行したいSQL(UPDATEで更新):
        #     # sql_insert = 'UPDATE umacopi_raceinfo SET date = ?'
        #     # sql_insert = 'UPDATE umacopi_racetable SET race_number = ?'
        #     sql_insert = 'UPDATE umacopi_raceresults SET rank = ?, frame=?, umaban = ?, rev_umaban = ?, horse_name = ?, odds = ?, popularity = ? WHERE horse_name = ?'
        
        # conn = sqlite3.connect(self.dbname)
        # cur = conn.cursor()
        # cur.execute(sql, update_data)
        # conn.commit()
        # cur.close()
        # conn.close()
        # '''


if __name__ == '__main__':
    # args = sys.argv
    # raceinfo = RaceInfoAnalyzer(args[1])
    # raceinfo.scraping_shutuba_table(args[2], args[3], args[4], int(args[5]))
    # raceinfo.scraping_race_result()

    args = sys.argv
    saveinfo = DbManager('/root/test/umacopi/web/db.sqlite3', args[1], args[2], args[3], args[4], int(args[5]))
    saveinfo.aaa()