from data_comparator import DataComparator
import sqlite3


class DbManager():
    def __init__(self, venue, date):
        self.dbname = '/root/test/umacopi/web/db.sqlite3'
        self.venue = venue
        self.date = date


        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        # 開催場所テーブル（指定時の一回のみDB問い合わせ ⇒ データがなければINSERT実行）
        sql_venue = 'SELECT name FROM umacopi_mstvenue WHERE name = ?'
        venue = cur.execute(sql_venue, (self.venue,)) # 第二引数は要素一つでもタプルで記述(,が必要)
        venue = venue.fetchone()
        if venue == None:
            print('umacopi_mstvenueテーブルに（開催場所を）インサート')
            sql_insert = 'INSERT INTO umacopi_mstvenue ([name]) VALUES(?)'
            cur.execute(sql_insert, (self.venue,))

        # レース情報テーブル（指定時の一回のみDB問い合わせ ⇒ データがなければINSERT実行）
        self.venue_id = cur.execute('SELECT id FROM umacopi_mstvenue WHERE name = ?', (self.venue,))
        self.venue_id = self.venue_id.fetchone()
        self.venue_id = self.venue_id[0] # id抽出
        
        sql_raceinfo = 'SELECT date, venue_id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?'
        raceinfo = cur.execute(sql_raceinfo, (self.date, self.venue_id))
        raceinfo = raceinfo.fetchone()

        if raceinfo == None:
            print('umacopi_raceinfoテーブルに（日付, 開催場所を）インサート')
            sql_insert = 'INSERT INTO umacopi_raceinfo ([date], [venue_id]) VALUES(?, ?)'
            cur.execute(sql_insert, (self.date, self.venue_id))

        conn.commit()
        cur.close()
        conn.close()


    def save_db(self, data):
        self.shutuba_table = data
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        # select_path = 'sql_select.txt'
        # insert_path = 'sql_insert.txt'
        for new_row in self.shutuba_table.itertuples(name=None): # 出走馬一頭単位で保存処理開始
            # with open(select_path) as f:
            # for sql_select in f:
            # sql_select = sql_select.strip()

            sql_umacopi_mstjockey = 'SELECT name FROM umacopi_mstjockey WHERE name = ?'
            jockey = cur.execute(sql_umacopi_mstjockey, (new_row[10],))
            jockey = jockey.fetchone()
            sql_umacopi_mstmark = 'SELECT kind FROM umacopi_mstmark WHERE kind = ?'
            mark = cur.execute(sql_umacopi_mstmark, (new_row[8],))
            mark = mark.fetchone()
            sql_umacopi_mststable = 'SELECT name FROM umacopi_mststable WHERE name = ?'
            stable = cur.execute(sql_umacopi_mststable, (new_row[11],))
            stable = stable.fetchone()

            if jockey == None:
                print('umacopi_mstjockeyに（騎手を）インサートします')
                sql_insert = 'INSERT INTO umacopi_mstjockey ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_row[10],))

            if mark == None:
                print('umacopi_mstmarkに（印を）インサートします')
                sql_insert = 'INSERT INTO umacopi_mstmark ([kind]) VALUES(?)'
                cur.execute(sql_insert, (new_row[8],))

            if stable == None:
                print('umacopi_mststableに（厩舎を）インサートします')
                sql_insert = 'INSERT INTO umacopi_mststable ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_row[11],))

# 作業用 ([0]9, [1]'2022/01/30', [2]'佐賀競馬場', [3]'11R', [4]'--'(着順), [5]8(枠), 
# 作業用  [6]10(馬番), [7]1(逆番), [8]'--'(印), [9]'オイカケマショウ', [10]'長田進仁', [11]'佐賀 中野博', [12]244.1, [13]10(人気)) 

# =============================     umacopi_racetable
            raceinfo_id = cur.execute('SELECT id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?', (self.date, self.venue_id))
            raceinfo_id = raceinfo_id.fetchone()
            raceinfo_id = raceinfo_id[0]

            sql_umacopi_racetable = 'SELECT race_num, raceinfo_id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?'
            racetable = cur.execute(sql_umacopi_racetable, (new_row[3], raceinfo_id))
            racetable = racetable.fetchone()
            if racetable == None:
                print('umacopi_racetableに（出馬表を）インサートします')
                sql_insert = 'INSERT INTO umacopi_racetable ([race_num], [raceinfo_id]) VALUES(?, ?)'
                cur.execute(sql_insert, (new_row[3], raceinfo_id))

    # =========================     umacopi_raceresults
            jockey_id = cur.execute('SELECT id FROM umacopi_mstjockey WHERE name = ?', (new_row[10],))
            jockey_id = jockey_id.fetchone()
            jockey_id = jockey_id[0]
            
            mark_id = cur.execute('SELECT id FROM umacopi_mstmark WHERE kind = ?', (new_row[8],))
            mark_id = mark_id.fetchone()
            mark_id = mark_id[0]

            racetable_id = cur.execute('SELECT id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?', (new_row[3], raceinfo_id))
            racetable_id = racetable_id.fetchone()
            racetable_id = racetable_id[0]

            stable_id = cur.execute('SELECT id FROM umacopi_mststable WHERE name = ?', (new_row[11],))
            stable_id = stable_id.fetchone()
            stable_id = stable_id[0]

            select_umacopi_raceresults = 'SELECT * FROM umacopi_raceresults WHERE umaban = ? AND racetable_id = ?'
            raceresults = cur.execute(select_umacopi_raceresults, (new_row[6], racetable_id))
            raceresults = raceresults.fetchone()

            if raceresults:
                old_data = (
                    raceresults[1], raceresults[6], raceresults[7], jockey_id, mark_id
                    ) # 更新前の情報
            new_data = (new_row[4], new_row[12], new_row[13], jockey_id, mark_id) # 更新後の情報

            data_comparator = DataComparator()
            if raceresults == None:
                sql_insert = 'INSERT INTO umacopi_raceresults ([rank],[frame],[umaban],[rev_umaban],[horse_name],[odds],[popularity],[jockey_id],[mark_id],[racetable_id],[stable_id]) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                insert_data = (
                    new_row[4], new_row[5], new_row[6], new_row[7], new_row[9], new_row[12], new_row[13], 
                    jockey_id, mark_id, racetable_id, stable_id
                    )
                cur.execute(sql_insert, insert_data)
                message_counts = 0

            else:
                if not data_comparator.compare_data(new_data, old_data): # 差異あり
                    sql_update = 'UPDATE umacopi_raceresults SET rank = ?, odds = ?, popularity = ?, jockey_id = ?, mark_id = ? WHERE umaban = ? AND racetable_id = ?'
                    update_data = (
                        new_data[0], new_data[1], new_data[2], jockey_id, mark_id, # UPDATE句の引数
                        new_row[6], racetable_id # WHERE句の引数
                        )
                    cur.execute(sql_update, update_data)
                    message_counts = 1
                else:
                    message_counts = 2
        
        if message_counts == 0:
            print('※ 新規データを追加しました。', '\n')
        elif message_counts == 1:
            print('※ 既存データを更新しました。', '\n')
        else:
            print('※ 更新はありません。', '\n')

        conn.commit()
        cur.close()
        conn.close()