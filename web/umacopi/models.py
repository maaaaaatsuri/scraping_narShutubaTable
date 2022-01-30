from django.db import models

# Create your models here.

class MstVenue(models.Model): # 開催場所テーブル
    name = models.CharField(max_length=10, verbose_name='開催場所名')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "開催場所"


class MstJockey(models.Model): # 騎手テーブル
    name = models.CharField(max_length=10, verbose_name='騎手名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "騎手"


class MstStable(models.Model): # 厩舎テーブル
    name = models.CharField(max_length=10, verbose_name='厩舎名')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "厩舎"


class MstMark(models.Model): # 印テーブル
    kind = models.CharField(max_length=10, verbose_name='印の種類')

    def __str__(self):
        return self.kind

    class Meta:
        verbose_name_plural = "印"


# 以下、トランザクションテーブル
class RaceInfo(models.Model): # 『レース情報』テーブル(一開催日＋一開催場所当りの情報を特定)
    date = models.CharField(max_length=12, verbose_name='開催日') # 開催日
    venue = models.ForeignKey(MstVenue, on_delete=models.CASCADE, verbose_name='開催場所') # 開催場所

    class Meta:
        verbose_name_plural = "レース情報"


class RaceTable(models.Model): # 『出馬表』テーブル(一レース当りの情報を特定)
    raceinfo = models.ForeignKey(RaceInfo, on_delete=models.CASCADE, verbose_name="レース情報") # レース情報ID
    race_num = models.CharField(max_length=4, null=True, blank=True, verbose_name='レース') # レース番号(01R~max12R)

    class Meta:
        verbose_name_plural = "出馬表"


class RaceResults(models.Model): # 『出走情報』テーブル(出走馬一頭当りの情報を特定)
    racetable = models.ForeignKey(RaceTable, on_delete=models.CASCADE, verbose_name="出馬表") # 出馬表ID
    rank = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='着順') # 着順(1~max18)
    frame = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='枠') # 枠(1~max8)
    umaban = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='馬番') # 馬番(1~max18)
    rev_umaban = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='逆番') # 逆番(1~max18)
    horse_name = models.CharField(max_length=10, verbose_name='馬名') # 馬名
    jockey = models.ForeignKey(MstJockey, on_delete=models.CASCADE, verbose_name="騎手") # 騎手ID
    stable = models.ForeignKey(MstStable, on_delete=models.CASCADE, verbose_name="厩舎") # 厩舎ID
    mark = models.ForeignKey(MstMark, on_delete=models.CASCADE, verbose_name="印") # 印ID
    odds = models.FloatField(null=True, blank=True, verbose_name='単勝オッズ') # 単勝オッズ(1.0~max999.9)
    popularity = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='人気') # 人気(1~max18)

    class Meta:
        verbose_name_plural = "レース結果"







# class NarModel(models.Model):
#     held_date = models.CharField(verbose_name='開催日', max_length=12)
#     venue = models.CharField(verbose_name='開催場所', max_length=10)
#     race_number = models.CharField(verbose_name='レース', max_length=4)
#     rank = models.PositiveSmallIntegerField(verbose_name='着順', null=True, blank=True)
#     frame = models.PositiveSmallIntegerField(verbose_name='枠', null=True, blank=True)
#     umaban = models.PositiveSmallIntegerField(verbose_name='馬番', null=True, blank=True)
#     rev_umaban = models.PositiveSmallIntegerField(verbose_name='逆番', null=True, blank=True)
#     mark = models.CharField(verbose_name='印', max_length=6)
#     horse_name = models.CharField(verbose_name='馬名', max_length=10)
#     jockey = models.CharField(verbose_name='騎手', max_length=10)
#     stable = models.CharField(verbose_name='厩舎', max_length=10)
#     odds = models.FloatField(verbose_name='単勝オッズ', null=True, blank=True)
#     popularity = models.PositiveSmallIntegerField(verbose_name='人気', null=True, blank=True)

#     def __str__(self):
#         return self.held_date