#!/usr/bin/env bash

CSV_FILE=$1
PEM_FILE=$2
LOG_FILE="failed_checks.log"
ENTRIES_NUM=0
> $LOG_FILE

parse_results() {
  LOG_FILE=$2
  COMPLETE_COUNT=0
  FAIL_COUNT=0

  CURRENT_IP=""
  FAILED_REASON=""

  while IFS= read -r line; do
    if [[ $line =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
      CURRENT_IP=$line
      FAILED_REASON=""
    elif [[ $line == *"[COMPLETE]"* ]]; then
      COMPLETE_COUNT=$((COMPLETE_COUNT + 1))
    elif [[ $line == *"[FAILED]"* ]]; then
      FAIL_COUNT=$((FAIL_COUNT + 1))
      FAILED_REASON="[BAD] Unexpected Reason."
    elif [[ $line == *"[BAD]"* ]]; then
      FAILED_REASON="${line}"
    fi

    if [[ $line == *"[FAILED]"* && -n $FAILED_REASON ]]; then
      echo "IP $CURRENT_IP failed because: $FAILED_REASON"
    fi
  done < "$LOG_FILE"

  echo "==================Summary of Failures=================="
  echo "$FAIL_COUNT/$1 servers failed."
}

while IFS=',' read -r IP _rest; do
  echo "==================checking ${IP}=================="
  ENTRIES_NUM=$((ENTRIES_NUM + 1))
  echo $IP >> "$LOG_FILE"
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash -s" < ./check.sh "$IP" | tee -a "$LOG_FILE"
done <"$CSV_FILE"

parse_results $ENTRIES_NUM $LOG_FILE

rm -f "$LOG_FILE"