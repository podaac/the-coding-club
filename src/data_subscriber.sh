# !/bin/bash

COLLECTION_NAME="AMSR2-REMSS-L2P-v8a"
START_DATE="2022-07-07T00:00:00Z"
OUTPUT_DIR="/AMSR2/REMSS/v8a"
LOG_FILE="/logs/${COLLECTION_NAME}_cron.log"
ERROR_LOG="/logs/${COLLECTION_NAME}_error.log"

echo "============== `/usr/bin/date` ===============" >> $LOG_FILE
echo "============== `/usr/bin/date` ===============" >> $ERROR_LOG

start=`date +%s`
podaac-data-subscriber -c $COLLECTION_NAME -d $OUTPUT_DIR -e .nc -dydoy -sd $START_DATE --verbose >> $LOG_FILE 2>> $ERROR_LOG
end=`date +%s`
elapsed=`expr $end - $start`
current_time=`date "+%Y-%m-%d %H:%M:%S.%3N"`
echo -e "[${current_time}] {${COLLECTION_NAME}_CRON} INFO - Execution time: ${elapsed} seconds.\n" >> $LOG_FILE
exit 0