from pyinfra import host, local
from pyinfra.operations import apt, server, files, git

git.repo(
    name="Clone CheckML repository",
    src="https://github.com/prosyslab-classroom/checkml.git",
    dest="/checkml",
    branch="main",
)

server.shell(
    name="build CheckML",
    commands=[
        "./build.sh",
    ],
    _sudo_user="student",
    _sudo_password="1234",
    _chdir="/checkml",
    _env={'OPAMSWITCH': 'checkml-5.1.0', 'OPAMYES': '1'},
)

server.shell(
    name="install CheckML executable",
    commands=[
        "cp /checkml/_build/default/src/main.exe /usr/bin/checkml"
    ],
    _sudo_user="student",
    _sudo_password="1234",
)

