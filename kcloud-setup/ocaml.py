from pyinfra import host
from pyinfra.operations import apt, server, files, git
from pyinfra.facts.server import Command

OCAML_VERSION = "5.1.0"
OPAM_SWITCH = f"prosyslab-classroom-{OCAML_VERSION}"

server.shell(
    name="init opam",
    commands=[
        f'opam init --compiler={OCAML_VERSION} --disable-sandboxing',
    ],
    _sudo_user="student",
    _sudo_password="1234",
    _env={'OPAMYES': '1'}
)

server.shell(
    name="create switch",
    commands=[
        f'opam switch create {OPAM_SWITCH} --package=ocaml-variants.{OCAML_VERSION}+options,ocaml-option-flambda',
    ],
    _ignore_errors=True, # Ignore error if switch already exists,
    _sudo_user="student",
    _sudo_password="1234",
    _env={'OPAMYES': '1'},
)

# Update .bashrc for student user
bashrc_content = host.get_fact(Command, command='cat /home/student/.bashrc')
if f'opam switch {OPAM_SWITCH}' not in bashrc_content:
    files.line(
        name="ensure opam switch is set",
        path="/home/student/.bashrc",
        line=f"opam switch {OPAM_SWITCH}",
        present=True,
    )
    files.line(
        name="ensure opam env is set",
        path="/home/student/.bashrc",
        line='''eval "$(opam env)"''',
        present=True,
    )

# Install OCaml packages
server.shell(
    name="install ocaml packages",
    commands=[
        f'opam install -y utop dune llvm ounit merlin ocamlformat=0.26.0 ocaml-lsp-server odoc z3 ocamlgraph core bisect_ppx',
        'opam pin add git+https://github.com/prosyslab-classroom/checkml.git',
        f'opam pin add git+https://github.com/prosyslab-classroom/llvmutils.git',
        f'opam pin add prosys-cil https://github.com/prosyslab/cil.git',
    ],
    _timeout=60 * 60, # an hour
    _sudo_user="student",
    _sudo_password="1234",
    _env={'OPAMYES': '1', 'OPAMSWITCH': OPAM_SWITCH},
)
