from pyinfra import host
from pyinfra.operations import apt, files, git, server

# Define LLVM version
LLVM_VERSION = 15

# Install LLVM packages
apt.packages(
    name="Install LLVM packages",
    packages=[
        f"libllvm-{LLVM_VERSION}-ocaml-dev",
        f"libllvm{LLVM_VERSION}",
        f"llvm-{LLVM_VERSION}",
        f"llvm-{LLVM_VERSION}-dev",
        f"llvm-{LLVM_VERSION}-doc",
        f"llvm-{LLVM_VERSION}-examples",
        f"llvm-{LLVM_VERSION}-runtime",
        "libzstd-dev",
        f"clang-{LLVM_VERSION}",
        f"clang-tools-{LLVM_VERSION}",
        f"clang-{LLVM_VERSION}-doc",
        f"libclang-common-{LLVM_VERSION}-dev",
        f"libclang-{LLVM_VERSION}-dev",
        f"libclang1-{LLVM_VERSION}",
        f"clang-format-{LLVM_VERSION}",
        f"python3-clang-{LLVM_VERSION}",
        f"clangd-{LLVM_VERSION}",
        f"libfuzzer-{LLVM_VERSION}-dev",
        f"lldb-{LLVM_VERSION}",
        f"lld-{LLVM_VERSION}",
        f"libc++-{LLVM_VERSION}-dev",
        f"libc++abi-{LLVM_VERSION}-dev",
    ],
    cache_time=60 * 60 * 24,  # every 24 hours,
    _parallel=4,
)


server.shell(
    name="Ensure LLVM system default",
    commands=[
        f"""update-alternatives \
  --install /usr/lib/llvm llvm /usr/lib/llvm-{LLVM_VERSION} 20 \
  --slave /usr/bin/llvm-ar llvm-ar /usr/bin/llvm-ar-{LLVM_VERSION} \
  --slave /usr/bin/llvm-as llvm-as /usr/bin/llvm-as-{LLVM_VERSION} \
  --slave /usr/bin/llvm-bcanalyzer llvm-bcanalyzer /usr/bin/llvm-bcanalyzer-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cat llvm-cat /usr/bin/llvm-cat-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cfi-verify llvm-cfi-verify /usr/bin/llvm-cfi-verify-{LLVM_VERSION} \
  --slave /usr/bin/llvm-config llvm-config /usr/bin/llvm-config-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cov llvm-cov /usr/bin/llvm-cov-{LLVM_VERSION} \
  --slave /usr/bin/llvm-c-test llvm-c-test /usr/bin/llvm-c-test-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cvtres llvm-cvtres /usr/bin/llvm-cvtres-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cxxdump llvm-cxxdump /usr/bin/llvm-cxxdump-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cxxfilt llvm-cxxfilt /usr/bin/llvm-cxxfilt-{LLVM_VERSION} \
  --slave /usr/bin/llvm-cxxmap llvm-cxxmap /usr/bin/llvm-cxxmap-{LLVM_VERSION} \
  --slave /usr/bin/llvm-diff llvm-diff /usr/bin/llvm-diff-{LLVM_VERSION} \
  --slave /usr/bin/llvm-dis llvm-dis /usr/bin/llvm-dis-{LLVM_VERSION} \
  --slave /usr/bin/llvm-dlltool llvm-dlltool /usr/bin/llvm-dlltool-{LLVM_VERSION} \
  --slave /usr/bin/llvm-dwarfdump llvm-dwarfdump /usr/bin/llvm-dwarfdump-{LLVM_VERSION} \
  --slave /usr/bin/llvm-dwp llvm-dwp /usr/bin/llvm-dwp-{LLVM_VERSION} \
  --slave /usr/bin/llvm-elfabi llvm-elfabi /usr/bin/llvm-elfabi-{LLVM_VERSION} \
  --slave /usr/bin/llvm-exegesis llvm-exegesis /usr/bin/llvm-exegesis-{LLVM_VERSION} \
  --slave /usr/bin/llvm-extract llvm-extract /usr/bin/llvm-extract-{LLVM_VERSION} \
  --slave /usr/bin/llvm-lib llvm-lib /usr/bin/llvm-lib-{LLVM_VERSION} \
  --slave /usr/bin/llvm-link llvm-link /usr/bin/llvm-link-{LLVM_VERSION} \
  --slave /usr/bin/llvm-lto2 llvm-lto2 /usr/bin/llvm-lto2-{LLVM_VERSION} \
  --slave /usr/bin/llvm-lto llvm-lto /usr/bin/llvm-lto-{LLVM_VERSION} \
  --slave /usr/bin/llvm-mc llvm-mc /usr/bin/llvm-mc-{LLVM_VERSION} \
  --slave /usr/bin/llvm-mca llvm-mca /usr/bin/llvm-mca-{LLVM_VERSION} \
  --slave /usr/bin/llvm-modextract llvm-modextract /usr/bin/llvm-modextract-{LLVM_VERSION} \
  --slave /usr/bin/llvm-mt llvm-mt /usr/bin/llvm-mt-{LLVM_VERSION} \
  --slave /usr/bin/llvm-nm llvm-nm /usr/bin/llvm-nm-{LLVM_VERSION} \
  --slave /usr/bin/llvm-objcopy llvm-objcopy /usr/bin/llvm-objcopy-{LLVM_VERSION} \
  --slave /usr/bin/llvm-objdump llvm-objdump /usr/bin/llvm-objdump-{LLVM_VERSION} \
  --slave /usr/bin/llvm-opt-report llvm-opt-report /usr/bin/llvm-opt-report-{LLVM_VERSION} \
  --slave /usr/bin/llvm-pdbutil llvm-pdbutil /usr/bin/llvm-pdbutil-{LLVM_VERSION} \
  --slave /usr/bin/llvm-PerfectShuffle llvm-PerfectShuffle /usr/bin/llvm-PerfectShuffle-{LLVM_VERSION} \
  --slave /usr/bin/llvm-profdata llvm-profdata /usr/bin/llvm-profdata-{LLVM_VERSION} \
  --slave /usr/bin/llvm-ranlib llvm-ranlib /usr/bin/llvm-ranlib-{LLVM_VERSION} \
  --slave /usr/bin/llvm-rc llvm-rc /usr/bin/llvm-rc-{LLVM_VERSION} \
  --slave /usr/bin/llvm-readelf llvm-readelf /usr/bin/llvm-readelf-{LLVM_VERSION} \
  --slave /usr/bin/llvm-readobj llvm-readobj /usr/bin/llvm-readobj-{LLVM_VERSION} \
  --slave /usr/bin/llvm-rtdyld llvm-rtdyld /usr/bin/llvm-rtdyld-{LLVM_VERSION} \
  --slave /usr/bin/llvm-size llvm-size /usr/bin/llvm-size-{LLVM_VERSION} \
  --slave /usr/bin/llvm-split llvm-split /usr/bin/llvm-split-{LLVM_VERSION} \
  --slave /usr/bin/llvm-stress llvm-stress /usr/bin/llvm-stress-{LLVM_VERSION} \
  --slave /usr/bin/llvm-strings llvm-strings /usr/bin/llvm-strings-{LLVM_VERSION} \
  --slave /usr/bin/llvm-strip llvm-strip /usr/bin/llvm-strip-{LLVM_VERSION} \
  --slave /usr/bin/llvm-symbolizer llvm-symbolizer /usr/bin/llvm-symbolizer-{LLVM_VERSION} \
  --slave /usr/bin/llvm-tblgen llvm-tblgen /usr/bin/llvm-tblgen-{LLVM_VERSION} \
  --slave /usr/bin/llvm-undname llvm-undname /usr/bin/llvm-undname-{LLVM_VERSION} \
  --slave /usr/bin/llvm-xray llvm-xray /usr/bin/llvm-xray-{LLVM_VERSION}""",
        # clang
        f"""update-alternatives \
  --install /usr/bin/clang clang /usr/bin/clang-{LLVM_VERSION} 10 \
  --slave /usr/bin/clang++ clang++ /usr/bin/clang++-{LLVM_VERSION} \
  --slave /usr/bin/clang-apply-replacements clang-apply-replacements /usr/bin/clang-apply-replacements-{LLVM_VERSION} \
  --slave /usr/bin/clang-change-namespace clang-change-namespace /usr/bin/clang-change-namespace-{LLVM_VERSION} \
  --slave /usr/bin/clang-check clang-check /usr/bin/clang-check-{LLVM_VERSION} \
  --slave /usr/bin/clang-cl clang-cl /usr/bin/clang-cl-{LLVM_VERSION} \
  --slave /usr/bin/clang-cpp clang-cpp /usr/bin/clang-cpp-{LLVM_VERSION} \
  --slave /usr/bin/clangd clangd /usr/bin/clangd-{LLVM_VERSION} \
  --slave /usr/bin/clang-extdef-mapping clang-extdef-mapping /usr/bin/clang-extdef-mapping-{LLVM_VERSION} \
  --slave /usr/bin/clang-format clang-format /usr/bin/clang-format-{LLVM_VERSION} \
  --slave /usr/bin/clang-format-diff clang-format-diff /usr/bin/clang-format-diff-{LLVM_VERSION} \
  --slave /usr/bin/clang-import-test clang-import-test /usr/bin/clang-import-test-{LLVM_VERSION} \
  --slave /usr/bin/clang-include-fixer clang-include-fixer /usr/bin/clang-include-fixer-{LLVM_VERSION} \
  --slave /usr/bin/clang-offload-bundler clang-offload-bundler /usr/bin/clang-offload-bundler-{LLVM_VERSION} \
  --slave /usr/bin/clang-query clang-query /usr/bin/clang-query-{LLVM_VERSION} \
  --slave /usr/bin/clang-refactor clang-refactor /usr/bin/clang-refactor-{LLVM_VERSION} \
  --slave /usr/bin/clang-rename clang-rename /usr/bin/clang-rename-{LLVM_VERSION} \
  --slave /usr/bin/clang-reorder-fields clang-reorder-fields /usr/bin/clang-reorder-fields-{LLVM_VERSION} \
  --slave /usr/bin/scan-view scan-view /usr/bin/scan-view-{LLVM_VERSION} \
  --slave /usr/bin/scan-build scan-build /usr/bin/scan-build-{LLVM_VERSION} \
  --slave /usr/bin/scan-build-py scan-build-py /usr/bin/scan-build-py-{LLVM_VERSION} \
  --slave /usr/bin/bugpoint bugpoint /usr/bin/bugpoint-{LLVM_VERSION} \
  --slave /usr/bin/c-index-test c-index-test /usr/bin/c-index-test-{LLVM_VERSION} \
  --slave /usr/bin/diagtool diagtool /usr/bin/diagtool-{LLVM_VERSION} \
  --slave /usr/bin/find-all-symbols find-all-symbols /usr/bin/find-all-symbols-{LLVM_VERSION} \
  --slave /usr/bin/git-clang-format git-clang-format /usr/bin/git-clang-format-{LLVM_VERSION} \
  --slave /usr/bin/hmaptool hmaptool /usr/bin/hmaptool-{LLVM_VERSION} \
  --slave /usr/bin/modularize modularize /usr/bin/modularize-{LLVM_VERSION} \
  --slave /usr/bin/obj2yaml obj2yaml /usr/bin/obj2yaml-{LLVM_VERSION} \
  --slave /usr/bin/opt opt /usr/bin/opt-{LLVM_VERSION} \
  --slave /usr/bin/sancov sancov /usr/bin/sancov-{LLVM_VERSION} \
  --slave /usr/bin/sanstats sanstats /usr/bin/sanstats-{LLVM_VERSION} \
  --slave /usr/bin/verify-uselistorder verify-uselistorder /usr/bin/verify-uselistorder-{LLVM_VERSION} \
  --slave /usr/bin/wasm-ld wasm-ld /usr/bin/wasm-ld-{LLVM_VERSION} \
  --slave /usr/bin/yaml2obj yaml2obj /usr/bin/yaml2obj-{LLVM_VERSION} \
  --slave /usr/bin/yaml-bench yaml-bench /usr/bin/yaml-bench-{LLVM_VERSION} \
  --slave /usr/bin/lld lld /usr/bin/lld-{LLVM_VERSION} \
  --slave /usr/bin/lld-link lld-link /usr/bin/lld-link-{LLVM_VERSION} \
  --slave /usr/bin/lli-child-target lli-child-target /usr/bin/lli-child-target-{LLVM_VERSION} \
  --slave /usr/bin/lli lli /usr/bin/lli-{LLVM_VERSION} \
  --slave /usr/bin/lldb lldb /usr/bin/lldb-{LLVM_VERSION} \
  --slave /usr/bin/lldb-argdumper lldb-argdumper /usr/bin/lldb-argdumper-{LLVM_VERSION} \
  --slave /usr/bin/lldb-mi lldb-mi /usr/bin/lldb-mi-{LLVM_VERSION} \
  --slave /usr/bin/lldb-server lldb-server /usr/bin/lldb-server-{LLVM_VERSION} \
  --slave /usr/bin/lldb-test lldb-test /usr/bin/lldb-test-{LLVM_VERSION} \
  --slave /usr/bin/lldb-vscode lldb-vscode /usr/bin/lldb-vscode-{LLVM_VERSION}""",
        # make system default
        f"""update-alternatives --install /usr/bin/cc cc /usr/bin/clang 100 && \
update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++ 100
""",
    ],
)
