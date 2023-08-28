#!/usr/bin/env bash

CSV_FILE=$1
PEM_FILE=$2

while IFS=',' read IP _rest; do
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash -s" < ./setup.sh &
done <$CSV_FILE
wait
