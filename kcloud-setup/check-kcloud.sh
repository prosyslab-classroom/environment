#!/usr/bin/env bash

CSV_FILE=""
PEM_FILE=""
RETRY=0
LOG_FILE="failed_checks.log"
ENTRIES_NUM=0
> $LOG_FILE

double_check() {
  CSV_FILE=$1
  PEM_FILE=$2
  LOG_FILE=$3

  echo "Running check script to identify failures..."

  if [[ -f $LOG_FILE ]]; then
    echo "Re-running failed components based on check results..."
    
    while IFS= read -r line; do
      if [[ $line =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        current_ip=$line
      elif [[ $line =~ \[BAD\] ]]; then
        if [[ $line =~ "User 'student' does not exist" ]]; then
          echo "Creating student account on $current_ip"
          ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$current_ip "userdel -r student || true; useradd -ms /bin/bash student || true; sudo adduser student sudo; echo 'student:1234' | chpasswd"
        elif [[ $line =~ "Directory /home/student is not empty" ]]; then
          echo "Cleaning /home/student on $current_ip"
          ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$current_ip "rm -rf /home/student/*"
        elif [[ $line =~ "clang is not installed" ]]; then
          echo "Installing clang on $current_ip"
          ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$current_ip "sudo -H bash /tmp/install-llvm-toolchain.sh"
        elif [[ $line =~ "opam is not installed" ]]; then
          echo "Installing opam on $current_ip"
          ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$current_ip "sudo -u student -H bash /tmp/install-ocaml.sh"
        fi
      fi
    done < $LOG_FILE

    echo "All re-installations completed."
    echo "Please make sure to run the check script again to verify the changes."
  else
    echo "No failed checks found."
  fi
}


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
      if [ -z "$FAILED_REASON" ]; then
        FAILED_REASON="[BAD] Unexpected Reason."
      fi
    elif [[ $line == *"[BAD]"* ]]; then
      if [ -z "$FAILED_REASON" ]; then
        FAILED_REASON="${line}"
      else
        FAILED_REASON="Multiple errors detected."
      fi
    fi

    if [[ $line == *"[FAILED]"* && -n $FAILED_REASON ]]; then
      echo "IP $CURRENT_IP failed because: $FAILED_REASON"
    fi
  done < "$LOG_FILE"

  echo "==================Summary of Failures=================="
  echo "$FAIL_COUNT/$1 servers failed."
}

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

while IFS=',' read -r IP _rest; do
  echo "==================checking ${IP}=================="
  ENTRIES_NUM=$((ENTRIES_NUM + 1))
  echo $IP >> "$LOG_FILE"
  ssh -o StrictHostKeyChecking=no -i $PEM_FILE root@$IP "bash -s" < ./check.sh "$IP" | tee -a "$LOG_FILE"
done <"$CSV_FILE"

parse_results $ENTRIES_NUM $LOG_FILE

if [[ $RETRY -eq 1 ]]; then
  double_check $CSV_FILE $PEM_FILE $LOG_FILE
fi

echo "All checks completed."

rm -f $LOG_FILE
