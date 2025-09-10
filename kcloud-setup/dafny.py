from pyinfra import host
from pyinfra.facts.server import Which
from pyinfra.operations import apt, files, server

# apt.packages(
#     name="Dafny dependencies",
#     packages=["dotnet-sdk-8.0"]
# )

if not host.get_fact(Which, "dafny", _sudo_user="student", _sudo_password="1234"):
    files.download(
        name="download dafny",
        src="https://github.com/dafny-lang/dafny/releases/download/v4.10.0/dafny-4.10.0-x64-ubuntu-20.04.zip",
        dest="/dafny-4.10.0-x64-ubuntu-20.04.zip",
        cache_time=60 * 60 * 24 * 7,  # 1 week
    )

    server.shell(
        name="Install Dafny",
        commands=[
            "yes | unzip /dafny-4.10.0-x64-ubuntu-20.04.zip -d /",
            'echo "export PATH=/dafny:$PATH" >> /home/student/.bashrc',
        ],
        _chdir="/",
    )

    files.line(
        name="ensure dafny is in PATH",
        path="/home/student/.bashrc",
        line="export PATH=/dafny:$PATH",
        present=True,
    )
