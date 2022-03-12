#!/bin/bash
cd /root/test/umacopi/backend/umacopi/umacopi_pack/

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
TODAY=`date '+%d'`
TOMORROW=`date '+%d' --date '1 days'`
HOUR=`date '+%H'`
MINUTE=`date '+%M'`


if [[ $HOUR%3 -eq 0 && $MINUTE -lt 30 ]]; then
    for VENUE in `cat venue.txt`
        do
            echo `date '+%Y/%m/%d %H:%M:%S'`
            echo $VENUE
            python3 umacopi.py $VENUE $YEAR $MONTH $TOMORROW 1
        done
else
    for VENUE in `cat venue.txt`
        do
            echo `date '+%Y/%m/%d %H:%M:%S'`
            echo $VENUE
            python3 umacopi.py $VENUE $YEAR $MONTH $TODAY 1
        done
fi