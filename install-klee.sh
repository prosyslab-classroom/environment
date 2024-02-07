#!/usr/bin/env bash

apt-get install build-essential cmake curl file g++-multilib gcc-multilib git libcap-dev libgoogle-perftools-dev libncurses5-dev libsqlite3-dev libtcmalloc-minimal4 python3-pip unzip graphviz doxygen libunwind-dev python3-tabulate z3
pip3 install lit wllvm

cd ~
git clone https://github.com/klee/klee.git
cd klee
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make

echo "export PATH=$PATH:~/klee/build/bin" >>~/.bashrc