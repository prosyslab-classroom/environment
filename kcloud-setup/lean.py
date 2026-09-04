from pyinfra.operations import apt, files, git, server

LEAN_VERSION = "4.32.2"
LEAN_PLATFORM = "linux"
LEAN_ARCHIVE = f"lean-{LEAN_VERSION}-{LEAN_PLATFORM}.tar.zst"
LEAN_ROOT = f"/opt/lean-{LEAN_VERSION}-{LEAN_PLATFORM}"
CHECKLEAN_ROOT = "/checklean"

apt.packages(
    name="Install Lean archive dependency",
    packages=["zstd"],
    update=True,
)

files.download(
    name=f"Download Lean {LEAN_VERSION}",
    src=(
        f"https://github.com/leanprover/lean4/releases/download/"
        f"v{LEAN_VERSION}/{LEAN_ARCHIVE}"
    ),
    dest=f"/tmp/{LEAN_ARCHIVE}",
    cache_time=60 * 60 * 24 * 7,
)

server.shell(
    name=f"Install Lean {LEAN_VERSION} system-wide",
    commands=[
        f'test -x "{LEAN_ROOT}/bin/lean" || '
        f'tar --use-compress-program=unzstd -xf "/tmp/{LEAN_ARCHIVE}" -C /opt',
        f'ln -sf "{LEAN_ROOT}/bin/lean" /usr/local/bin/lean',
        f'ln -sf "{LEAN_ROOT}/bin/lake" /usr/local/bin/lake',
        f'ln -sf "{LEAN_ROOT}/bin/leanc" /usr/local/bin/leanc',
        f'/usr/local/bin/lean --version | grep -qF "version {LEAN_VERSION}"',
    ],
)

git.repo(
    name="Clone checklean repository",
    src="https://github.com/prosyslab-classroom/checklean",
    dest=CHECKLEAN_ROOT,
    branch="main",
)

server.shell(
    name="Build and install checklean",
    commands=[
        "lake build check-lean",
        "install -m 0755 .lake/build/bin/check-lean /usr/local/bin/checklean",
    ],
    _chdir=CHECKLEAN_ROOT,
)

files.line(
    name="Ensure /usr/local/bin is in the student login PATH",
    path="/home/student/.profile",
    line='export PATH="/usr/local/bin:$PATH"',
    present=True,
)

files.line(
    name="Ensure /usr/local/bin is in the student interactive PATH",
    path="/home/student/.bashrc",
    line='export PATH="/usr/local/bin:$PATH"',
    present=True,
)

server.shell(
    name="Verify checklean is available to the student user",
    commands=[
        "sudo -u student -H bash -lc "
        "'test \"$(command -v checklean)\" = \"/usr/local/bin/checklean\"'",
    ],
)
