#!/usr/bin/env bash
ROOT=$(dirname $(dirname $(realpath $0)))
CSV_FILE=""
PEM_FILE=""
RETRY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    -r|--retry)
      RETRY=1
      shift
      ;;
    *)
      if [[ -z "$CSV_FILE" ]]; then
        CSV_FILE=$1
      elif [[ -z "$PEM_FILE" ]]; then
        PEM_FILE=$1
      else
        echo "Unexpected argument: $1"
        exit 1
      fi
      shift 
      ;;
  esac
done

if [[ -z "$CSV_FILE" || -z "$PEM_FILE" ]]; then
  echo "Usage: $0 [-r|--retry] <CSV_FILE> <PEM_FILE>"
  exit 1
fi
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

if [ $RETRY -eq 1 ]; then
  bash $ROOT/kcloud-setup/check-kcloud.sh $CSV_FILE $PEM_FILE --retry
else
  bash $ROOT/kcloud-setup/check-kcloud.sh $CSV_FILE $PEM_FILE
fi
