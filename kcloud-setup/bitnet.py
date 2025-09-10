from pyinfra import host
from pyinfra.facts.server import Which
from pyinfra.operations import apt, files, git, server

# Ensure python3-pip and git are available
apt.packages(
    name="Install BitNet dependencies (pip, git)",
    packages=["python3-pip", "git"],
    update=True,
)

# Clone BitNet repository
git.repo(
    name="Clone BitNet repository",
    src="https://github.com/prosyslab-classroom/BitNet",
    dest="/BitNet",
    branch="main",
    recursive=True,
)

# Install Python requirements
server.shell(
    name="Install BitNet Python requirements",
    commands=[
        "pip3 install -r requirements.txt",
    ],
    _chdir="/BitNet",
)

# Ensure huggingface hub cli is available
server.shell(
    name="Install huggingface hub CLI",
    commands=[
        "pip3 install --upgrade 'huggingface_hub[cli]'",
    ],
)

# Download the model files
server.shell(
    name="Download BitNet model (gguf)",
    commands=[
        "mkdir -p models/BitNet-b1.58-2B-4T",
        "command -v hf >/dev/null 2>&1 && hf download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T || huggingface-cli download microsoft/BitNet-b1.58-2B-4T-gguf --local-dir models/BitNet-b1.58-2B-4T",
    ],
    _chdir="/BitNet",
)

# Run environment setup
server.shell(
    name="Run BitNet environment setup",
    commands=[
        "python3 setup_env.py -md models/BitNet-b1.58-2B-4T -q i2_s",
    ],
    _chdir="/BitNet",
)

# Ensure run_inference.sh is executable and symlinked
server.shell(
    name="Set run_inference.sh executable and create symlink",
    commands=[
        "chmod 755 run_inference.sh",
        "ln -sf /BitNet/run_inference.sh /usr/local/bin/run_inference",
    ],
    _chdir="/BitNet",
)
