# Setup KCloud Machines

```
./setup-kcloud.sh $MACHINE_LIST_CSV_FILE $PEM_KEY_FILE
```

For example, `./setup-kcloud.sh is593.csv IS593A.pem` would install packages in the machines listed
in `is593.csv` file. Note that the csv file (`$MACHINE_LIST_CSV_FILE`) must be single column table with the NAT_IPs of the machines
