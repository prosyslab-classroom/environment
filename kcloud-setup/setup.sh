#!/usr/bin/env bash

add-apt-repository -y ppa:avsm/ppa
apt-get install -y make git gcc ocaml opam dune pkg-config m4 cmake sudo python2.7 libgmp-dev python3-distutils g++

# Install souffle
wget https://souffle-lang.github.io/ppa/souffle-key.public -O /usr/share/keyrings/souffle-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | sudo tee /etc/apt/sources.list.d/souffle.list
apt update
apt install -y souffle

# Install llvm
sudo -H bash /tmp/install-llvm-toolchain.sh

# Add user
userdel -r student || true
useradd -ms /bin/bash student || true

sudo adduser student sudo
echo "student:1234" | chpasswd

# Setup opam
echo 1234 | sudo -S apt-get -y install curl
cd /home/student
sudo -u student -H bash /tmp/install-ocaml.sh

# Setup checkml
cd /
apt-get install -y libtree-sitter-dev cargo nodejs
sudo git clone https://github.com/prosyslab-classroom/checkml.git 
sudo cd checkml && sudo -u student -H bash ./build.sh
sudo cp _build/default/src/main.exe /usr/bin/checkml
