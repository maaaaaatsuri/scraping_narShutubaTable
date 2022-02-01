cd /root/HorseRacingAnalyzer/backend/umacopi/umacopi_pack

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
DAY=`date '+%d'`

echo `date '+%Y/%m/%d %H:%M:%S'`
python3 umacopi.py "佐賀競馬場" $YEAR $MONTH $DAY 1