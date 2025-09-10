from pyinfra.operations import apt, files, git, server

server.shell(
    name="ensure student is not a sudoer",
    commands=["deluser student sudo"],
)
