from pyinfra import host, local
from pyinfra.facts.server import Which
from pyinfra.operations import apt, files, git, server

if not host.get_fact(Which, "souffle", _sudo_user="student", _sudo_password="1234"):
    apt.key(
        name="Add Soufflé public key",
        src="https://souffle-lang.github.io/ppa/souffle-key.public",
        keyid="/usr/share/keyrings/souffle-archive-keyring.gpg",
    )

    apt.repo(
        name="Add Soufflé repository",
        src="deb [signed-by=/usr/share/keyrings/souffle-archive-keyring.gpg] https://souffle-lang.github.io/ppa/ubuntu/ stable main",
        filename="souffle",
    )

    apt.packages(
        name="Ensure Soufflé is installed",
        packages=["souffle"],
        _parallel=4,
    )
