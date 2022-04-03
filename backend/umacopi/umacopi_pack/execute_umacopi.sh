#!/bin/bash
cd /root/umacopi/backend/umacopi/umacopi_pack/

YEAR=`date '+%Y'`
MONTH=`date '+%m'`
NEXT_MONTH_FIRST=`date '+%Y %m 01' -d "1 months"`
TODAY=`date '+%d'`
TOMORROW=`date '+%d' --date '1 days'`
HOUR=`date '+%H'`
MINUTE=`date '+%M'`


if [[ $HOUR%3 -eq 0 && $MINUTE -lt 30 ]]; then #【3の倍数】時ちょうどの時は、翌日の情報をスクレイピング
    if [[ $TODAY -lt $TOMORROW ]]; then # 当日が月末ではない場合、翌日のレース情報をスクレイピング
        for VENUE in `cat venue.txt`
            do
                echo `date '+%Y %m 01' -d '`date '+%Y-%m-01'` 1 months'`
                echo $VENUE
                python3 umacopi.py $VENUE $YEAR $MONTH $TOMORROW 1
            done
    else # 当日が月末の場合、翌月1日のレース情報をスクレイピング
        for VENUE in `cat venue.txt`
            do
                echo `date '+%Y/%m/%d %H:%M:%S'`
                echo $VENUE
                python3 umacopi.py $VENUE $NEXT_MONTH_FIRST 1
            done
    fi
else # 当日のレース情報をスクレイピング
    for VENUE in `cat venue.txt`
        do
            echo `date '+%Y/%m/%d %H:%M:%S'`
            echo $VENUE
            python3 umacopi.py $VENUE $YEAR $MONTH $TODAY 1
        done
fi