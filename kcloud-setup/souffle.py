from pyinfra.operations import apt, files, server

SOUFFLE_VERSION = "2.5"
SOUFFLE_DEB = f"x86_64-ubuntu-2404-souffle-{SOUFFLE_VERSION}-Linux.deb"
SOUFFLE_DEB_PATH = f"/var/tmp/{SOUFFLE_DEB}"
# SHA-256 of the official GitHub release asset downloaded over HTTPS.
SOUFFLE_SHA256 = "c7e9dd1349506bbb23c4dcf89e87396198006235f79b1cc516c0a2b67ac067bc"

files.download(
    name=f"Download Soufflé {SOUFFLE_VERSION} for Ubuntu 24.04",
    src=f"https://github.com/souffle-lang/souffle/releases/download/{SOUFFLE_VERSION}/{SOUFFLE_DEB}",
    dest=SOUFFLE_DEB_PATH,
    sha256sum=SOUFFLE_SHA256,
    mode="644",
    _parallel=4,
)

apt.update(
    name="Refresh apt indexes for Soufflé dependencies",
    _parallel=4,
)

apt.deb(
    name=f"Install Soufflé {SOUFFLE_VERSION}",
    src=SOUFFLE_DEB_PATH,
    _parallel=4,
)

server.shell(
    name="Verify Soufflé package version and executable",
    commands=[
        f'test "$(dpkg-query -W -f=\'${{Version}}\' souffle)" = "{SOUFFLE_VERSION}"',
        "souffle --version",
    ],
)
