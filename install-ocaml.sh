#!/bin/bash

export OCAML_VERSION=4.13.1
export OPAM_SWITCH=prosyslab-classroom-$OCAML_VERSION
export OPAMYES=1

if [[ $SHLVL -gt 2 ]]; then
    opam init github git+https://github.com/ocaml/opam-repository.git
else
    opam init --compiler=$OCAML_VERSION --disable-sandboxing
fi

opam switch create $OPAM_SWITCH --package=ocaml-variants.$OCAML_VERSION+options,ocaml-option-flambda

eval $(opam env)
opam install -y utop dune llvm.13.0.0 ounit merlin ocamlformat=0.26.0 ocaml-lsp-server odoc z3 ocamlgraph core bisect_ppx.2.8.1
opam pin add git+https://github.com/prosyslab-classroom/llvmutils.git
opam pin add git+https://github.com/prosyslab/cil

echo "opam switch $OPAM_SWITCH" >>~/.bashrc
echo "eval \$(opam env)" >>~/.bashrc
