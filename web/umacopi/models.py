from django.db import models

# Create your models here.

class NarModel(models.Model):
    held_date = models.CharField(verbose_name='開催日', max_length=12)
    venue = models.CharField(verbose_name='開催場所', max_length=10)
    race_number = models.CharField(verbose_name='レース', max_length=4)
    rank = models.PositiveSmallIntegerField(verbose_name='着順', null=True, blank=True)
    frame = models.PositiveSmallIntegerField(verbose_name='枠', null=True, blank=True)
    umaban = models.PositiveSmallIntegerField(verbose_name='馬番', null=True, blank=True)
    rev_umaban = models.PositiveSmallIntegerField(verbose_name='逆番', null=True, blank=True)
    mark = models.CharField(verbose_name='印', max_length=6)
    horse_name = models.CharField(verbose_name='馬名', max_length=10)
    jockey = models.CharField(verbose_name='騎手', max_length=10)
    stable = models.CharField(verbose_name='厩舎', max_length=10)
    odds = models.FloatField(verbose_name='単勝オッズ', null=True, blank=True)
    popularity = models.PositiveSmallIntegerField(verbose_name='人気', null=True, blank=True)

    def __str__(self):
        return self.held_date



"""
class NarModel(models.Model):
    held_date = models.CharField(max_length=12)
    venue = models.CharField(max_length=10)
    race_number = models.CharField(max_length=4)
    rank = models.PositiveSmallIntegerField(null=True, blank=True)
    frame = models.PositiveSmallIntegerField(null=True, blank=True)
    umaban = models.PositiveSmallIntegerField(null=True, blank=True)
    rev_umaban = models.PositiveSmallIntegerField(null=True, blank=True)
    mark = models.CharField(max_length=6)
    horse_name = models.CharField(max_length=10)
    jockey = models.CharField(max_length=10)
    stable = models.CharField(max_length=10)
    odds = models.FloatField(null=True, blank=True)
    popularity = models.PositiveSmallIntegerField(null=True, blank=True)
"""



"""
class MstVenue(models.Model): # 競馬場テーブル
    venue_id = models.PositiveSmallIntegerField(primary_key=True) # 競馬場ID
    venue = models.CharField(max_length=10) # 競馬場名

class MstJockey(models.Model): # 騎手テーブル
    jockey_id = models.PositiveSmallIntegerField(primary_key=True) # 騎手ID
    jockey = models.CharField(max_length=10) # 騎手名

class MstStable(models.Model): # 厩舎テーブル
    stable_id = models.PositiveSmallIntegerField(primary_key=True) # 厩舎ID
    stable = models.CharField(max_length=10) # 厩舎名

class MstMark(models.Model): # 印テーブル
    mark_id = models.PositiveSmallIntegerField(primary_key=True) # 印ID
    mark = models.CharField(max_length=10) # 印表示

# 以下、トランザクションテーブル

class HeldInfo(models.Model): # 開催情報テーブル(開催情報(「いつ行われる、どの競馬場の全レース」が対象であるか)を特定)
    # held_id = models.PositiveIntegerField(primary_key=True) # 開催情報管理番号(1~∞)

    date = models.CharField(max_length=12) # 開催日
    venue_id = models.ForeignKey(Venue) # 競馬場ID

    class RaceTable(models.Model): # 出馬表テーブル(出馬表を特定)
    # race_table_id = PositiveIntegerField(primary_key=True) # 出馬表管理番号(1~∞)

    # held_id = models.ForeignKey(Venue) # 開催情報管理番号(1~∞)
    race_num = models.CharField(max_length=4, null=True, blank=True) # レース番号(01R~max12R)


class RaceResults(models.Model): # 出走情報テーブル(出走情報を特定)
    # RaceHorse = models.PositiveIntegerField(primary_key=True) # 出走情報管理番号(1~∞)

    # race_table_id = PositiveIntegerField(primary_key=True) # 出馬表管理番号(1~∞)
    rank = models.PositiveSmallIntegerField(null=True, blank=True) # 着順(1~max18)
    frame = models.PositiveSmallIntegerField(null=True, blank=True) # 枠(1~max8)
    umaban = models.PositiveSmallIntegerField(null=True, blank=True) # 馬番(1~max18)
    rev_umaban = models.PositiveSmallIntegerField(null=True, blank=True) # 逆番(1~max18)
    horse_name = models.CharField(max_length=10) # 馬名
    jockey_id = models.ForeignKey(Jockey) # 騎手ID
    stable_id = models.ForeignKey(Stable) # 厩舎ID
    mark_id = models.ForeignKey(Mark) # 印ID
    odds = models.FloatField(null=True, blank=True) # 単勝オッズ(1.1~max999.9)
    popularity = models.PositiveSmallIntegerField(null=True, blank=True) # 人気(1~max18)
"""
