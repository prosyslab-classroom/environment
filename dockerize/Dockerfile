FROM ubuntu:22.04

# Disabled due to unstable connection
# RUN sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y software-properties-common && \
    apt-get install -y make git gcc ocaml pkg-config m4 cmake sudo python2.7 libgmp-dev python3-distutils curl wget opam vim \
    # For checkml
    libtree-sitter-dev cargo nodejs

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

# Setup checkml
WORKDIR /
USER root
RUN git clone https://github.com/prosyslab-classroom/checkml.git 
RUN cd checkml && ./build.sh
RUN cp /checkml/_build/default/src/main.exe /usr/bin/checkml

# Clean up
RUN rm -rf $SCRIPT
USER student
WORKDIR $HOME