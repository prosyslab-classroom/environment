#!/usr/bin/env bash
ROOT=$(dirname $(dirname $(realpath $0)))
CSV_FILE=$1
PEM_FILE=$2

echo "Start Copying setup scripts to the servers"

# copy scripts to /tmp of each server instance iteratively
while IFS=',' read IP _rest; do
  scp -o StrictHostKeyChecking=no -i $PEM_FILE $ROOT/kcloud-setup/setup.sh $ROOT/install-ocaml.sh $ROOT/install-llvm-toolchain.sh root@$IP:/tmp/
 done <$CSV_FILE
wait

echo "Start running the setup scripts"

# Then, run them parallely 
while IFS=',' read IP _rest; do
  echo "Running setup script on ${IP}"
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash /tmp/setup.sh" &
done <$CSV_FILE
wait