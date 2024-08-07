#!/usr/bin/env bash
ROOT=$(dirname $(dirname $(realpath $0)))
CSV_FILE=$1
PEM_FILE=$2

while IFS=',' read IP _rest; do
  scp -o StrictHostKeyChecking=no -i $PEM_FILE $ROOT/kcloud-setup/setup.sh $ROOT/install-ocaml.sh $ROOT/install-llvm-toolchain.sh root@$IP:/tmp/
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash /tmp/setup.sh" &
  # ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash -s" < ./setup.sh &
done <$CSV_FILE
wait
