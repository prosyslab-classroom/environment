#!/usr/bin/env bash

CSV_FILE=$1
PEM_FILE=$2

while IFS=',' read IP _rest; do
  echo $IP
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash -s" < ./check.sh
done <$CSV_FILE
