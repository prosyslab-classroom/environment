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



## Using Pyinfra

```bash
# pyinfra [inventory] [operations]
pyinfra cs348.py deploy.py --no-wait -y
```

* Operations which download packages from `apt` have a limited parallelism due to their rate-limit policy.
* `--no-wait` let remote machines not wait for other machines to finish the same operation
    - By default, `pyinfra` synchronizes operations across all remote machines in `[inventory]`

### When you want to go to bed

Most of the time, setup fails due to network failure.
This is because an apt repository might block you for a while since you are actually DOS-attacking the server with 100+ machines.
Therefore, it is not your fault. You just need more time to bypass the rate-limit.
This is a helpful to tip to keep the setup process working even if you go to bed.

```bash
until pyinfra cs348.py deploy.py -y; do
    echo "retry..."
    sleep 600; # The apt repository might not want you to come back too early...
end
```

Moreover, some machines can be slow to build some packages or just hang while building for unknown reasons.
(it takes a notorious amount of time to build `z3` opam package, especially).
Therefore, I recommend for you to set timeout to such processes.
I already set timeout for `z3` case, but you need to keep looking at such process.

```python
# ocaml.py

# Install OCaml packages
server.shell(
    name="install ocaml packages",
    commands=[
        f'opam install -y utop dune llvm ounit merlin ocamlformat=0.26.0 ocaml-lsp-server odoc z3 ocamlgraph core bisect_ppx',
        f'opam pin add git+https://github.com/prosyslab-classroom/llvmutils.git',
        f'opam pin add prosys-cil https://github.com/prosyslab/cil.git',
    ],
    _timeout=60 * 60, # an hour
    _sudo_user="student",
    _sudo_password="1234",
    _env={'OPAMYES': '1', 'OPAMSWITCH': OPAM_SWITCH},
)
```



Also, you can check if processes are running in host machines with:

```bash
pyinfra cs348.py exec -- 'ps aux | grep "opam install" | grep -v "grep"'
```
