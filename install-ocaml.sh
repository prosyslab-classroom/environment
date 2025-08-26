#!/bin/bash

export OCAML_VERSION=5.2.0
export OPAM_SWITCH=prosyslab-classroom-$OCAML_VERSION
export OPAMYES=1

set -e

if [[ $SHLVL -gt 2 ]]; then
    opam init github git+https://github.com/ocaml/opam-repository.git
else
    opam init --compiler=$OCAML_VERSION --disable-sandboxing
fi

# if the switch is already there, skip
if ! opam switch list -s | grep -q "^$OPAM_SWITCH\$"; then
    opam switch create $OPAM_SWITCH --package=ocaml-variants.$OCAML_VERSION+options,ocaml-option-flambda
fi

eval $(SHELL=bash opam env --switch=$OPAM_SWITCH)
opam install -y utop dune llvm ounit merlin ocamlformat ocaml-lsp-server odoc z3 ocamlgraph core bisect_ppx ocurl
opam pin add git+https://github.com/prosyslab-classroom/llvmutils.git
opam pin add prosys-cil https://github.com/prosyslab/cil.git
opam pin add git+https://github.com/prosyslab-classroom/checkml.git

echo "opam switch $OPAM_SWITCH" >>~/.bashrc
echo "eval \$(opam env)" >>~/.bashrc
