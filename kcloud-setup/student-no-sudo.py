from pyinfra.operations import apt, server, files, git

server.shell(
    name="ensure student is not a sudoer",
    commands=["deluser student sudo"],
)