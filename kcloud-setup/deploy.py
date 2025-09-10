from pyinfra import host, local
from pyinfra.operations import apt, files, git, server

local.include("system-setup.py")
local.include("llvm.py")
local.include("ocaml.py")
local.include("checkml.py")
local.include("dafny.py")
local.include("souffle.py")
local.include("bitnet.py")
