from io import StringIO

from pyinfra.operations import apt, files, git, server

BITNET_ENV = {"PATH": "/BitNet/.venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"}

# Install venv support without modifying the system Python environment
apt.packages(
    name="Install BitNet dependencies (pip, venv, build tools)",
    packages=["python3-pip", "python3.12-venv", "cmake", "clang", "git", "make", "g++"],
    update=True,
    cache_time=60 * 60 * 24,  # update every 24 hours,
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
        "/BitNet/.venv/bin/python -m pip install 'huggingface_hub[cli]<1.0'",
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

# Download the Qwen model used by the inference wrappers
server.shell(
    name="Download Qwen2.5-Coder-3B model (gguf)",
    commands=[
        "/BitNet/.venv/bin/hf download Qwen/Qwen2.5-Coder-3B-Instruct-GGUF --local-dir models/Qwen2.5-Coder-3B-Instruct",
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

files.directory(
    name="Ensure BitNet wrapper directory exists",
    path="/usr/local/libexec",
    user="root",
    group="root",
    mode="755",
)

# Keep the upstream launchers unchanged, but make their python3 use the venv.
for command in (
    "run_inference",
    "run_inference_server",
    "run_inference_qwen3b",
    "run_inference_server_qwen3b",
):
    server.shell(
        name=f"Make {command}.sh executable",
        commands=[f"chmod 755 /BitNet/{command}.sh"],
    )

    wrapper_path = f"/usr/local/libexec/bitnet-{command.replace('_', '-')}"
    files.put(
        name=f"Install BitNet {command} wrapper",
        src=StringIO(
            '#!/bin/sh\n'
            'export PATH="/BitNet/.venv/bin:$PATH"\n'
            f'exec /bin/bash /BitNet/{command}.sh "$@"\n'
        ),
        dest=wrapper_path,
        user="root",
        group="root",
        mode="755",
    )

    files.link(
        name=f"Expose BitNet {command} command",
        path=f"/usr/local/bin/{command}",
        target=wrapper_path,
    )
