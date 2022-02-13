from data_comparator import DataComparator
import sqlite3


class DbManager():
    def __init__(self, venue, date):
        self.dbname = '/root/test/umacopi/web/db.sqlite3'
        self.venue = venue
        self.date = date


    def save_db(self, data):
        self.shutuba_table = data
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        # 開催場所テーブル（指定時の一回のみDB問い合わせ ⇒ データがなければINSERT実行）
        sql_venue = 'SELECT name FROM umacopi_venue WHERE name = ?'
        venue = cur.execute(sql_venue, (self.venue,)) # 第二引数は要素一つでもタプルで記述(,が必要)
        venue = venue.fetchone()
        if venue == None:
            print('『開催場所』テーブルに、新規の開催場所【', venue, '】を登録しました。')
            sql_insert = 'INSERT INTO umacopi_venue ([name]) VALUES(?)'
            cur.execute(sql_insert, (self.venue,))

        # レース情報テーブル（指定時の一回のみDB問い合わせ ⇒ データがなければINSERT実行）
        self.venue_id = cur.execute('SELECT id FROM umacopi_venue WHERE name = ?', (self.venue,))
        self.venue_id = self.venue_id.fetchone()
        self.venue_id = self.venue_id[0] # id抽出        
        sql_raceinfo = 'SELECT date, venue_id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?'
        raceinfo = cur.execute(sql_raceinfo, (self.date, self.venue_id))
        raceinfo = raceinfo.fetchone()
        if raceinfo == None:
            print('『レース情報』テーブルに【', raceinfo, '】を登録しました。')
            sql_insert = 'INSERT INTO umacopi_raceinfo ([date], [venue_id]) VALUES(?, ?)'
            cur.execute(sql_insert, (self.date, self.venue_id))

        for new_row in self.shutuba_table.itertuples(name=None): # 出走馬一頭単位で保存処理開始
            new_race_num = new_row[3]
            new_rank = new_row[4]
            new_frame = new_row[5]
            new_umaban = new_row[6]
            new_rev_umaban = new_row[7]
            new_mark = new_row[8]
            new_horse_name = new_row[9]
            new_jockey = new_row[10]
            new_stable = new_row[11]
            new_odds = new_row[12]
            new_popularity = new_row[13]

            sql_umacopi_jockey = 'SELECT name FROM umacopi_jockey WHERE name = ?'
            jockey = cur.execute(sql_umacopi_jockey, (new_jockey,))
            jockey = jockey.fetchone()
            if jockey == None:
                print('『騎手』テーブルに、新規の騎手【', jockey, '】を登録しました。')
                sql_insert = 'INSERT INTO umacopi_jockey ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_jockey,))
                
            sql_umacopi_mark = 'SELECT kind FROM umacopi_mark WHERE kind = ?'
            mark = cur.execute(sql_umacopi_mark, (new_mark,))
            mark = mark.fetchone()
            if mark == None:
                print('『印』テーブルに、新規の印【', mark, '】を登録しました。')
                sql_insert = 'INSERT INTO umacopi_mark ([kind]) VALUES(?)'
                cur.execute(sql_insert, (new_mark,))

            sql_umacopi_stable = 'SELECT name FROM umacopi_stable WHERE name = ?'
            stable = cur.execute(sql_umacopi_stable, (new_stable,))
            stable = stable.fetchone()
            if stable == None:
                print('『厩舎』テーブルに、新規の厩舎【', stable, '】を登録しました。')
                sql_insert = 'INSERT INTO umacopi_stable ([name]) VALUES(?)'
                cur.execute(sql_insert, (new_stable,))

# =============================     umacopi_racetable
            raceinfo_id = cur.execute('SELECT id FROM umacopi_raceinfo WHERE date = ? AND venue_id = ?', (self.date, self.venue_id))
            raceinfo_id = raceinfo_id.fetchone()
            raceinfo_id = raceinfo_id[0]
            sql_umacopi_racetable = 'SELECT race_num, raceinfo_id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?'
            racetable = cur.execute(sql_umacopi_racetable, (new_race_num, raceinfo_id))
            racetable = racetable.fetchone()
            if racetable == None:
                sql_insert = 'INSERT INTO umacopi_racetable ([race_num], [raceinfo_id]) VALUES(?, ?)'
                cur.execute(sql_insert, (new_race_num, raceinfo_id))

# =============================     umacopi_raceresults
            jockey_id = cur.execute('SELECT id FROM umacopi_jockey WHERE name = ?', (new_jockey,))
            jockey_id = jockey_id.fetchone()
            jockey_id = jockey_id[0]
            
            mark_id = cur.execute('SELECT id FROM umacopi_mark WHERE kind = ?', (new_mark,))
            mark_id = mark_id.fetchone()
            mark_id = mark_id[0]

            racetable_id = cur.execute('SELECT id FROM umacopi_racetable WHERE race_num = ? AND raceinfo_id = ?', (new_race_num, raceinfo_id))
            racetable_id = racetable_id.fetchone()
            racetable_id = racetable_id[0]

            stable_id = cur.execute('SELECT id FROM umacopi_stable WHERE name = ?', (new_stable,))
            stable_id = stable_id.fetchone()
            stable_id = stable_id[0]

            select_umacopi_raceresults = 'SELECT * FROM umacopi_raceresults WHERE umaban = ? AND racetable_id = ?'
            raceresults = cur.execute(select_umacopi_raceresults, (new_umaban, racetable_id))
            raceresults = raceresults.fetchone()

            if raceresults:
                old_data = (
                    raceresults[1], raceresults[6], raceresults[7], jockey_id, mark_id
                    ) # 更新前の情報
            new_data = (new_rank, new_odds, new_popularity, jockey_id, mark_id) # 更新後の情報

            data_comparator = DataComparator()
            if raceresults == None:
                sql_insert = 'INSERT INTO umacopi_raceresults ([rank],[frame],[umaban],[rev_umaban],[horse_name],[odds],[popularity],[jockey_id],[mark_id],[racetable_id],[stable_id]) VALUES(?,?,?,?,?,?,?,?,?,?,?)'
                insert_data = (
                    new_rank, new_frame, new_umaban, new_rev_umaban, new_horse_name, new_odds, new_popularity, 
                    jockey_id, mark_id, racetable_id, stable_id
                    )
                cur.execute(sql_insert, insert_data)
                message_counts = 0

            else:
                if not data_comparator.compare_data(new_data, old_data): # 差異あり
                    sql_update = 'UPDATE umacopi_raceresults SET rank = ?, odds = ?, popularity = ?, jockey_id = ?, mark_id = ? WHERE umaban = ? AND racetable_id = ?'
                    update_data = (
                        new_data[0], new_data[1], new_data[2], jockey_id, mark_id, # UPDATE句の引数
                        new_umaban, racetable_id # WHERE句の引数
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