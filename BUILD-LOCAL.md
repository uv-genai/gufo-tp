# Native TP2 build on the Strix Halo hosts

The active checkout is `/home/ugo/projects/gufo` on both hosts. Development
happens on `main` tracking `uv-genai/main`; the deployed peer checkout may have
local launcher changes, so do not reset or switch it merely to deploy a binary.
Read [AGENTS.md](AGENTS.md) and [handoff.md](handoff.md) for workflow and current
binary identity. Source-build prerequisites are in [README.md](README.md#build-from-source).

## Configure and build

Install Rust with rustup and the repository's pinned toolchain if it is absent:

```sh
export PATH="$HOME/.cargo/bin:$PATH"
rustup toolchain install 1.88.0 --profile minimal --component rustfmt --component clippy
```

If `rustup` is absent, install it from [rustup.rs](https://rustup.rs/).
PNG and WAV decoding require Cargo at configure/build time; the copied Gufo
executable does not require Rust on the peer host.

Use the system ROCm installation at `/opt/rocm`. Every configure on these hosts
needs the environment and all three host flags below. RDMA is disabled by
upstream default, so explicitly enable it for a new TP2 build directory.

```sh
cd /home/ugo/projects/gufo
unset ROCM_PATH
export PATH="$HOME/.cargo/bin:$PATH"
export PATH=/opt/rocm/bin:/opt/rocm/core/lib/llvm/bin:$PATH
cmake --preset release -DGUFO_ENABLE_TP2_RDMA=ON \
  -DCMAKE_HIP_COMPILER=/opt/rocm/core/lib/llvm/bin/clang++ \
  -DCMAKE_CXX_FLAGS="-include format" \
  -DCMAKE_HIP_FLAGS="-include format" \
  -DGUFO_REVISION="$(git rev-parse HEAD)"
cmake --build --preset release --parallel 4
# Run diagnosis when the GPU host is free:
./build/release/gufo diagnose
```

Commit code before building a binary that will be published or qualified.
`GUFO_REVISION` is cached by CMake: pass the source revision explicitly when
building changed code so `gufo --version` does not retain an older revision.
Documentation-only updates can retain the already validated binary; record its
compiled revision separately from the release tag in the handoff and notes.

| Symptom | Host workaround |
| --- | --- |
| `expected an identifier for the attribute name` in `<format>` | GCC 16's `<format>` collides with HIP's `__noinline__` macro; force-include `<format>` in both CXX and HIP flags |
| `Failed to find HIP root directory` | Put the system ROCm tools on PATH and pin the real HIP compiler path |
| `cannot find ROCm device library` | Unset `ROCM_PATH`; the symlinked package layout otherwise breaks device-library lookup |

These are host workarounds, not portable project settings; keep them out of
CMake presets. Preserve compiler/dependency versions for comparisons. The
November 6 qualification used GCC 16.2.1 and the system ROCm 10.1 toolchain.
The optional `build-gufo.sh` helper supplies the same host flags; use `JOBS=4`
and configure `GUFO_REVISION` explicitly as above for a newly committed build.

## Deploy and qualify

Keep one Gufo process per GPU host. Before replacing executables or launching
another model, coordinate with any running llama-swap session. Build on one
host, copy the same binary to the peer's `build/release/gufo`, and compare full
SHA-256 hashes. Preserve the peer's unrelated source/configuration edits.

Both hosts need the complete, identical target shards, MTP sidecar and projector.
Sync changed rank launchers as well as the binary. Follow
[TP2-SETUP.md](TP2-SETUP.md#part-d--running-the-two-host-server) and the
[merge checklist](docs/internal/MERGE-CHECKLIST.md) for generation, reuse and concurrency
checks. Successful compilation or HTTP readiness alone does not qualify TP2.
