FROM ubuntu:22.04

# Disabled due to unstable connection
# RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    apt-get install -y make git gcc ocaml pkg-config m4 cmake sudo python2.7 libgmp-dev python3-distutils curl wget opam vim zstd \
    # For checkml
    libtree-sitter-dev cargo nodejs \
    # For constrained-decoding
    python3-pip libcurl4-gnutls-dev

RUN wget https://souffle-lang.github.io/ppa/souffle-key.public -O /usr/share/keyrings/souffle-archive-keyring.gpg
RUN echo "deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main" | sudo tee /etc/apt/sources.list.d/souffle.list
RUN apt-get update
RUN apt-get install -y souffle

ENV HOME=/home/student

RUN useradd -ms /bin/bash student

ENV SCRIPT=$HOME/script
RUN mkdir -p $SCRIPT
COPY install-llvm-toolchain.sh $SCRIPT
RUN $SCRIPT/install-llvm-toolchain.sh

RUN sudo adduser student sudo
RUN echo "root:1234" | chpasswd
RUN echo "student:1234" | chpasswd
USER student

COPY install-ocaml.sh $SCRIPT
RUN $SCRIPT/install-ocaml.sh

# Make the checkml binary installed by install-ocaml.sh available system-wide
WORKDIR /
USER root
RUN install -m 0755 \
    /home/student/.opam/prosyslab-classroom-5.2.0/bin/checkml \
    /usr/local/bin/checkml

# Install dafny
RUN wget https://github.com/dafny-lang/dafny/releases/download/v4.10.0/dafny-4.10.0-x64-ubuntu-20.04.zip
RUN apt install -y dotnet-sdk-8.0
RUN unzip dafny-4.10.0-x64-ubuntu-20.04.zip
RUN rm dafny-4.10.0-x64-ubuntu-20.04.zip
RUN echo "export PATH=/dafny:\$PATH" >> /home/student/.bashrc
RUN ln -s /dafny/dafny /usr/local/bin/dafny

# Install huggingface
RUN pip3 install -U "huggingface_hub[cli]"
RUN echo "export PATH=$HOME/.local/bin:\$PATH" >> /home/student/.bashrc

# Setup BitNet
RUN git clone --recursive https://github.com/prosyslab-classroom/BitNet
WORKDIR /BitNet
RUN pip3 install -r requirements.txt
RUN hf download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T
RUN python3 setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s
RUN chmod 755 run_inference.sh
RUN ln -s /BitNet/run_inference.sh /usr/local/bin/run_inference

# Install Lean 4.32.2 and checklean
ARG LEAN_VERSION=4.32.2
ENV LEAN_ROOT=/opt/lean-${LEAN_VERSION}-linux
ENV PATH=/usr/local/bin:${PATH}

RUN wget "https://github.com/leanprover/lean4/releases/download/v${LEAN_VERSION}/lean-${LEAN_VERSION}-linux.tar.zst" \
      -O "/tmp/lean-${LEAN_VERSION}-linux.tar.zst" && \
    tar --use-compress-program=unzstd \
      -xf "/tmp/lean-${LEAN_VERSION}-linux.tar.zst" -C /opt && \
    rm -f "/tmp/lean-${LEAN_VERSION}-linux.tar.zst" && \
    ln -s "${LEAN_ROOT}/bin/lean" /usr/local/bin/lean && \
    ln -s "${LEAN_ROOT}/bin/lake" /usr/local/bin/lake && \
    ln -s "${LEAN_ROOT}/bin/leanc" /usr/local/bin/leanc && \
    lean --version | grep -qF "version ${LEAN_VERSION}"

WORKDIR /
RUN git clone https://github.com/prosyslab-classroom/checklean /checklean && \
    cd /checklean && \
    lake build check-lean && \
    install -m 0755 .lake/build/bin/check-lean /usr/local/bin/checklean

# Clean up
RUN rm -rf $SCRIPT
USER student
WORKDIR $HOME
