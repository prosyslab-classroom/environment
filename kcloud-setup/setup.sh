#!/usr/bin/env bash

# This disables interactive prompts such as "Pending kernel upgrade" or "Daemons using outdated libraries"
export DEBIAN_FRONTEND=noninteractive

# add-apt-repository -y ppa:avsm/ppa
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
echo 1234 | sudo -S apt-get -y install curl libcurl4-gnutls-dev
cd /home/student
sudo -u student -H bash /tmp/install-ocaml.sh

# Install dafny
cd /
sudo wget https://github.com/dafny-lang/dafny/releases/download/v4.10.0/dafny-4.10.0-x64-ubuntu-20.04.zip
sudo apt install -y dotnet-sdk-8.0
sudo dafny-4.10.0-x64-ubuntu-20.04.zip
sudo rm dafny-4.10.0-x64-ubuntu-20.04.zip
sudo echo "export PATH=/dafny:\$PATH" >> /home/student/.bashrc

# Install BitNet and model
apt-get install -y python3-pip

# Clone or update BitNet repository
if [ ! -d "/BitNet/.git" ]; then
  git clone --recursive https://github.com/prosyslab-classroom/BitNet /BitNet
else
  git -C /BitNet pull --ff-only || true
  git -C /BitNet submodule update --init --recursive || true
fi

cd /BitNet

# Install Python requirements
pip3 install -r requirements.txt

# Ensure Hugging Face CLI is available
pip3 install -U 'huggingface_hub[cli]' hf_transfer

# Download model (prefer `hf`, fallback to `huggingface-cli`)
mkdir -p models/BitNet-b1.58-2B-4T
if command -v hf >/dev/null 2>&1; then
  hf download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
else
  huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
fi

# Run environment setup
python3 setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s

# Make inference script executable and symlink to PATH
chmod 755 run_inference.sh
ln -sf /BitNet/run_inference.sh /usr/local/bin/run_inference

# Install Lean 4.32.2
LEAN_VERSION=4.32.2
LEAN_PLATFORM=linux
LEAN_ARCHIVE="lean-${LEAN_VERSION}-${LEAN_PLATFORM}.tar.zst"
LEAN_ROOT="/opt/lean-${LEAN_VERSION}-${LEAN_PLATFORM}"

apt-get install -y zstd

if [ ! -x "${LEAN_ROOT}/bin/lean" ]; then
  wget "https://github.com/leanprover/lean4/releases/download/v${LEAN_VERSION}/${LEAN_ARCHIVE}" -O "/tmp/${LEAN_ARCHIVE}"
  tar --use-compress-program=unzstd -xf "/tmp/${LEAN_ARCHIVE}" -C /opt
  rm -f "/tmp/${LEAN_ARCHIVE}"
fi

# Make Lean tools available system-wide, including to the student user
ln -sf "${LEAN_ROOT}/bin/lean" /usr/local/bin/lean
ln -sf "${LEAN_ROOT}/bin/lake" /usr/local/bin/lake
ln -sf "${LEAN_ROOT}/bin/leanc" /usr/local/bin/leanc
/usr/local/bin/lean --version | grep -qF "version ${LEAN_VERSION}"

# Clone or update checklean, build it, and install the executable system-wide
if [ ! -d "/checklean/.git" ]; then
  git clone https://github.com/prosyslab-classroom/checklean /checklean
else
  git -C /checklean pull --ff-only
fi

cd /checklean
lake build check-lean
install -m 0755 .lake/build/bin/check-lean /usr/local/bin/checklean

# Explicitly keep /usr/local/bin in the student's login and interactive PATH
grep -qxF 'export PATH="/usr/local/bin:$PATH"' /home/student/.profile || \
  echo 'export PATH="/usr/local/bin:$PATH"' >> /home/student/.profile
grep -qxF 'export PATH="/usr/local/bin:$PATH"' /home/student/.bashrc || \
  echo 'export PATH="/usr/local/bin:$PATH"' >> /home/student/.bashrc

sudo -u student -H bash -lc \
  'test "$(command -v checklean)" = "/usr/local/bin/checklean"'
