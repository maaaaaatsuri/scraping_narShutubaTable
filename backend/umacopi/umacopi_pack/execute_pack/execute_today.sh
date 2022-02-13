cd /root/test/umacopi/backend/umacopi/umacopi_pack/

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
DAY=`date '+%d'`


for VENUE in `cat venue.txt`
    do
        echo `date '+%Y/%m/%d %H:%M:%S'`
        echo $VENUE
        python3 umacopi.py $VENUE $YEAR $MONTH $DAY 1
    done
