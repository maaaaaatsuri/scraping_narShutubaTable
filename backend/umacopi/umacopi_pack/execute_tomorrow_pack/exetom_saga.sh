cd /root/HorseRacingAnalyzer/backend/umacopi/umacopi_pack

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
TOMORROW=`date '+%d' --date '1 days'`

echo `date '+%Y/%m/%d %H:%M:%S'`
python3 umacopi.py "佐賀競馬場" $YEAR $MONTH $TOMORROW 1