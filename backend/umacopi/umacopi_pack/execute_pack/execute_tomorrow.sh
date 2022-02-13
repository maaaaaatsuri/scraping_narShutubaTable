cd /root/test/umacopi/backend/umacopi/umacopi_pack/

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
TOMORROW=`date '+%d' --date '1 days'`


for VENUE in `cat venue.txt`
    do
        echo `date '+%Y/%m/%d %H:%M:%S'`
        echo $VENUE
        python3 umacopi.py $VENUE $YEAR $MONTH $TOMORROW 1
    done
