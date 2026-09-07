from io import StringIO

from pyinfra.operations import apt, files, git, server

BITNET_ENV = {"PATH": "/BitNet/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}

# Install venv support without modifying the system Python environment
apt.packages(
    name="Install BitNet dependencies (venv, git)",
    packages=["python3-venv", "git"],
    update=True,
    _parallel=4,
)

# Clone BitNet repository
git.repo(
    name="Clone BitNet repository",
    src="https://github.com/prosyslab-classroom/BitNet",
    dest="/BitNet",
    branch="main",
    update_submodules=True,
    recursive_submodules=True,
    _parallel=4,
)

# Keep Python dependencies isolated from Ubuntu's apt-managed Python.
server.shell(
    name="Create BitNet virtual environment",
    commands=["test -x /BitNet/.venv/bin/python || python3 -m venv /BitNet/.venv"],
    _parallel=4,
)

# Install Python requirements
server.shell(
    name="Install BitNet Python requirements",
    commands=[
        "/BitNet/.venv/bin/python -m pip install -r requirements.txt",
    ],
    _chdir="/BitNet",
    _env=BITNET_ENV,
    _parallel=4,
)

# Ensure huggingface hub cli is available
server.shell(
    name="Install huggingface hub CLI",
    commands=[
        "/BitNet/.venv/bin/python -m pip install --upgrade huggingface_hub",
    ],
    _parallel=4,
)

# Download the model files
server.shell(
    name="Download BitNet model (gguf)",
    commands=[
        "mkdir -p models/BitNet-b1.58-2B-4T",
        "/BitNet/.venv/bin/hf download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T",
    ],
    _chdir="/BitNet",
    _env=BITNET_ENV,
    _parallel=4,
)

# Run environment setup
server.shell(
    name="Run BitNet environment setup",
    commands=[
        "/BitNet/.venv/bin/python setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s",
    ],
    _chdir="/BitNet",
    _env=BITNET_ENV,
)

# Keep the upstream launcher unchanged, but make its python3 use the venv.
files.put(
    name="Install BitNet inference wrapper",
    src=StringIO(
        '#!/bin/sh\n'
        'export PATH="/BitNet/.venv/bin:$PATH"\n'
        'exec /bin/bash /BitNet/run_inference.sh "$@"\n'
    ),
    dest="/usr/local/libexec/bitnet-run-inference",
    user="root",
    group="root",
    mode="755",
)

files.link(
    name="Expose BitNet inference command",
    path="/usr/local/bin/run_inference",
    target="/usr/local/libexec/bitnet-run-inference",
)
