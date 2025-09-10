from pyinfra import host
from pyinfra.operations import apt, files, git, server

# List of required packages
SYSTEM_PACKAGES = [
    "make",
    "git",
    "gcc",
    "ocaml",
    "opam",
    "dune",
    "pkg-config",
    "m4",
    "cmake",
    "sudo",
    "python2.7",
    "libgmp-dev",
    "python3-distutils",
    "g++",
    "curl",
    # ocaml deps
    "zlib1g-dev"
    # dafny
    "dotnet-sdk-8.0",
]

apt.packages(
    name="Ensure essential system packages are installed",
    packages=SYSTEM_PACKAGES,
    update=True,
    cache_time=60 * 60 * 24,  # update every 24 hours,
    _parallel=4,  # Try not to DDOS the apt repository (you can be banned for a while)
)

server.user(
    name="Ensure student user exists",
    user="student",
    home="/home/student",
    shell="/bin/bash",
    present=True,
)

server.shell(
    name="Ensure student is in sudo group",
    commands=["adduser student sudo"],
)

server.shell(
    name="Set student password",
    commands=['echo "student:1234" | chpasswd'],
)
