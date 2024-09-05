#!/usr/bin/env bash

IP=$1
LOG="/tmp/check_log.txt"
check_student_account() {
  if id "student" &>/dev/null; then
    echo "[GOOD] User 'student' exists."
  else
    echo "[BAD] User 'student' does not exist on $IP."
    echo "account" >> $LOG
  fi
}

check_clean_userdir() {
  if [ "$(ls /home/student | wc -l)" -eq 0 ]; then
    echo "[GOOD] Directory /home/student is clean."
  else
    echo "[BAD] Directory /home/student is not empty on $IP."
    echo "clean" >> $LOG
  fi
}

check_clang() {
  if clang --version | grep -q "Ubuntu clang version 13.0.1-2ubuntu2.2"; then
    echo "[GOOD] clang is installed."
  else
    echo "[BAD] clang is not installed on $IP."
    echo "clang" >> $LOG
  fi
}

check_opam() {
  OPAM_SWITCH=prosyslab-classroom-4.13.1

  if sudo -u student -H bash -c "opam switch $OPAM_SWITCH; eval \$(opam env); opam list" | grep z3 >/dev/null; then
    echo "[GOOD] opam is installed."
  else
    echo "[BAD] opam is not installed on $IP."
    echo "opam" >> $LOG
  fi
}

check_souffle() {
  if souffle --version | grep -q "Souffle"; then
    echo "[GOOD] souffle is installed."
  else
    echo "[BAD] souffle is not installed on $IP."
  fi
}

check_student_account
check_clean_userdir
check_clang
check_opam
check_souffle

# if LOG is empty, then it means that everything is good
if [ ! -s $LOG ]; then
  echo "[COMPLETE] Everything is good on $IP."
else 
  echo "[FAILED] Something is wrong on $IP."
fi
