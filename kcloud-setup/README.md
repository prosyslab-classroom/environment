# Setup KCloud Machines

```
./setup-kcloud.sh $MACHINE_LIST_CSV_FILE $PEM_KEY_FILE
```

For example, `./setup-kcloud.sh is593.csv IS593A.pem` would install packages in the machines listed
in `is593.csv` file. Note that the csv file (`$MACHINE_LIST_CSV_FILE`) must be single column table with the NAT_IPs of the machines

# Checking if packages are well-setup

```
./check-kcloud.sh [OPTIONAL -r] $MACHINE_LIST_CSV_FILE $PEM_KEY_FILE
```
For example, `./setup-kcloud.sh is593.csv IS593A.pem` would check if each machines listed in `is593.csv` file have the following packages.

1. `student` user account
2. if `student` user account is empty
3. clang(llvm toolchain)
4. opam
5. souffle

If `-r` option is added, the script will attempt to reinstall the missing packages.
