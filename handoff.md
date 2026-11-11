# LIVE HANDOFF — Gufo-TP

Canonical file: `/home/ugo/projects/gufo/handoff.md`. Updated **2026-11-11** for
the v0.32.0 upstream integration; v0.33.0 follows on its own branch/PR. Latest published release remains
`tp2-rdma-fixes-v0.28.1-2026-11-06`. Edit this file after deployment,
merge, release or incident changes; dated files under `~/gufo-merge-handoff/`
are archives, and its lowercase `handoff.md` is only a pointer here.

## Read next

**Permanent model restriction:** never run Qwen3.8 27B Q8 again. Prioritize
Qwen3.8 Flash-Next, including its Q4/Q8 TP2 and MTP modes. Qwen3.8 27B Q4 is
permitted only for a specific, justified check. The restriction is on the 27B
Q8 model, not Flash-Next Q8. The earlier broad test queues were closed on November 6. Query live processes
before using either GPU; this document does not establish current availability.

1. [AGENTS.md](AGENTS.md): host flags, remotes and TP2 invariants.
2. [Upstream merge record](docs/internal/MERGE-UPSTREAM-2026-11-06.md): current integration and qualification.
   [Prior release notes](docs/releases/2026-11-06-tp2-fixes.md) describe the published v0.28.1 fixes.
3. [BUILD-LOCAL.md](BUILD-LOCAL.md) and [TP2-SETUP.md](TP2-SETUP.md): native build/deployment.
4. [Merge checklist](docs/internal/MERGE-CHECKLIST.md) and [TP2 design](docs/internal/models/qwen3.8-flash-next/TP2.md).

## Repository and release

| Item | Current state |
| --- | --- |
| Development | `/home/ugo/projects/gufo`, `main` tracks **`uv-genai/main`** |
| Publish remote | **`uv-genai` only**, `https://github.com/uv-genai/gufo-tp.git` |
| Upstream | `origin` → `gufo-org/gufo`, local tracking branch `gufo-org`; never push there |
| Upstream merged through | **v0.32.0** (`c40862ff`); v0.29–v0.31 were integrated through PRs [#29](https://github.com/uv-genai/gufo-tp/pull/29), [#30](https://github.com/uv-genai/gufo-tp/pull/30) and [#31](https://github.com/uv-genai/gufo-tp/pull/31); unreleased upstream main is excluded |
| Latest release | [tp2-rdma-fixes-v0.28.1-2026-11-06](https://github.com/uv-genai/gufo-tp/releases/tag/tp2-rdma-fixes-v0.28.1-2026-11-06) |
| Previous release | [tp2-rdma-merge-v0.28.1-2026-11-04](https://github.com/uv-genai/gufo-tp/releases/tag/tp2-rdma-merge-v0.28.1-2026-11-04), code `2a7c0262` |
| Review fixes | [PR #25](https://github.com/uv-genai/gufo-tp/pull/25), merged **`ba1ab427`**, closes #21–#24 |
| Q4 reader fix | [PR #27](https://github.com/uv-genai/gufo-tp/pull/27), merged **`ae8a93c3`**, closes #26 |
| Package version | `version.txt` is **0.32.0** from the upstream tag; the latest dated TP2 release remains based on v0.28.1 |

Separate branches and validated PRs precede code merges. Every published tag
must have a GitHub Release with written notes. Do not move published tags or
push upstream tags wholesale. See [release policy](docs/internal/releasing.md).
AGENTS.md is project-owned: its case-insensitive prohibited-environment name
count must remain zero; never run that package manager here. Windows is out of
scope for this release.

## Deployed binary and live service

Both hosts have `/home/ugo/projects/gufo/build/release/gufo`:

- Compiled revision **`251757aadea6bf9a03dfb8c4a86c4c351a02486c`**.
- SHA-256 **`ed942b606cf8ee241d705cf806bcac150c8600fe1d45df1d3409cc5829311936`**.
- Production code includes v0.31.0 provider metadata, legal prefill stops and
  mirrored reasoning controls, retaining the native TP snapshot path. New layer yields and decode overlap are gated to one host. Later
  commits change tests/documentation only. Source extension API is **0.2.17**.
- The binary reports `gufo version development (251757aa...)`. Do not confuse
  its compiled revision with the squash commit or the release documentation commit.
- The v0.30.0 baseline `7f0d93f2…` (SHA `9ad8a5a3…`) is retained on both
  hosts at `artifacts/upstream-2026-11-06/gufo-main-v0.30.0`.
- The v0.29.0 baseline `3ea5054d…` (SHA `43be5781…`) is retained on both
  hosts at `artifacts/upstream-2026-11-06/gufo-main-v0.29.0`.
- The v0.28.1 baseline `85ae8ce2…` (SHA `653edd21…`) is retained on both
  hosts at `artifacts/upstream-2026-11-06/gufo-main-v0.28.1`.
- Previous binary `37feeaad…` is retained on both hosts at
  `artifacts/q4-file-check-2026-11-06/gufo-before`; the November 4 binary
  `42aded09…` is at `artifacts/tp2-review-fixes-2026-11-06/gufo-main`.

The user's Q8 TP2 + MTP pair ran under llama-swap until an explicit UI unload
at **18:51 AWST on November 6**. The subsequent upstream qualification uses
isolated Q4/Q8 TP2 pairs, four sessions, context 524288 and static YaRN 2,
then leaves the GPUs unloaded. A worker reporting a closed control channel
at that unload time reflects the rank-0 shutdown, not a new generation failure.
Query processes, `/running`, `/metrics` and `/slots` for live state before GPU
work; preserve the user's current model selection and never load a second
model on either host.

| Role | Host | Entry |
| --- | --- | --- |
| Rank 0 / HTTP | `strix-halo-1.local`, `192.168.1.22` | system llama-swap service, `tools/llama-swap/tp2.sh` |
| Rank 1 / worker | `strix-halo-2.local` (this checkout) | started over SSH by the wrapper |

- Client API: `http://192.168.1.22:8080/v1`.
- Model IDs: `gufo-qwen3.8-flash-next-tp2-q4` / `gufo-qwen3.8-flash-next-tp2-q8`.
- Backend ports are assigned by llama-swap; **query `GET /running`**. The last
  Q8 run used 5802 and Q4 used 5801. These are observations, not fixed settings.
- Wrapper: `tools/llama-swap/tp2.sh run PORT q4|q8`; stop through the owning
  llama-swap entry. `tools/tp2/swap.sh` is an older wrapper, not the deployed entry.
- Rank defaults: **sessions 2, context 524288, YaRN 2, MTP**. These are capacity
  settings, not proof of full-depth context quality.
- Bootstrap/control: **18515 / 18516**. Both rank scripts must agree on token,
  model files, context, YaRN, sessions, MTP and projector.
- Rank 0 log: `~/gufo-tp2-swap.log`; rank 1: `~/tp2-rank1-swap.log`.
  Proxy logs: `journalctl -u llama-swap` on rank 0 (system service, not user unit).
- The peer checkout has unrelated local launcher/source changes; preserve them.
  Deploy identical binaries and changed launchers explicitly instead of resetting
  that checkout. Local `main` tracking `uv-genai/main` is the development base.

## Models and loader incident

Weights live under `~/.cache/models/Qwen3.8-Flash-Next/` on **both** hosts:
`Q8_0/` (six shards), `UD-Q4_K_XL/` (four shards),
`MTP/mtp-Qwen3.8-Flash-Next-shared-Q8_0.gguf`, and `mmproj-BF16.gguf`.

The re-downloaded Q4 set matches publisher revision
`d96201194f103c906994f283f504209dc8d2a10c` on both hosts. Its first shard is
**10,946,618 bytes and zero tensors**; all 1,224 tensors are in the other three.
Gufo's former padding check rejected it as `Malformed or truncated GGUF`.
The reader now accepts complete metadata-only shards without tensor padding;
truncated metadata and weight extents still fail. No model bytes were changed.
Hashes and download instructions: [model guide](docs/internal/models/qwen3.8-flash-next/README.md#metadata-only-q4-shard).
A preceding `peer closed the channel` launch failure was secondary to a missing
Q4 file on rank 1; inspect both rank logs before diagnosing a collective bug.

## Current upstream validation

The [November 11 merge record](docs/internal/MERGE-UPSTREAM-2026-11-11.md)
records 362 passing v0.32.0 TP2+MTP checks (Q4/Q8), CPU/operator checks and
retained inconclusive timing evidence. The large Q8 uncached timing outlier
did not recur in the unchanged-candidate diagnostic; its cause is unresolved.


See the [merge record](docs/internal/MERGE-UPSTREAM-2026-11-06.md) for v0.29.0 through v0.31.0
build, CPU/GPU tests, four TP2 modes and per-request timing controls. Raw
evidence is retained under the corresponding version directories in
`artifacts/upstream-2026-11-06/`.
TP protocol is **23**, snapshot payload is 20, and TP2 retains its mirrored
snapshot path with component caching disabled. Static YaRN has a distinct
persistence identity. Upgrade both hosts together; older peers are rejected.
Only compatible persisted states can restore.

The v0.31.0 binary passes **724 TP2 functional checks** across Q4/Q8 AR/MTP,
including 60 Q4 image checks, and the single-host Flash-Next Q4 AR/MTP suites.
Flash-Next single-host MTP has no timing flags; other retained timing flags are
advisory/inconclusive. Qwen27 Q4's completed controls have no confirmed slowdown
after including the final unchanged-main observation. Qwen27 Q8 candidate
qualification was interrupted and must not be resumed; DeepSeek GPU coverage
is unavailable. See the merge record for exact scope. All model-test queues
are closed; do not restart them to complete the broader discarded matrix.

## Prior v0.28.1 release validation and evidence

| Scope | Result / evidence |
| --- | --- |
| Current reader repair | Regression fails before/passes after; GGUF v2/v3, metadata/weight entry shards, truncated metadata and missing weight padding covered. Actual Q4 set opens from all four entry shards: 1,224 tensors / 4 mappings |
| CPU / repository | **80/80** locally and hosted Linux CI for PR #27; format **723/723** with clang-format 21 and 23; release build and docs check pass |
| Final binary Q4 | Actual llama-swap launch + PONG; **15** long-prefill/code/reuse/concurrency requests + **9** MTP tool/schema/streaming checks; 3,877-token prefill, exact replay with **85 cached tokens**, **2 active / 3 queued**, clean rank logs |
| Final binary Q8 | **5 post-merge generation checks**, actual MTP drafts; user's long runs complete normally |
| Earlier Q8 numerical fix | `c1e4cc38`: **3/3** attention/projection/routed operator suites and **171** AR/MTP functional checks (96 reasoning budgets, 18 long-context/cancellation, 48 cache/restart, 9 constraints) |
| Cache numerical epoch | `a40b1616`, SHA `37feeaad…`: **50** cache/upgrade checks including the old-binary primer + **9** MTP constraint checks |

Artifacts retained under the ignored repository `artifacts/` directory:

- `q4-file-check-2026-11-06/`: hashes, CPU reproduction, build and hosted logs,
  llama-swap launch, `q4-smoke/`, post-merge validation and both rank logs.
- `tp2-review-fixes-2026-11-06/`: earlier failing investigations, `validation-3/`,
  `final-cache-validation-1/`, operator probes and timing histories.
- `q8-stream-investigation-2026-11-06/`: rank/proxy logs and live slot samples.

Do not attribute every earlier suite to the final binary: the Q8 kernel/wire
fix was qualified first, the cache epoch next, then the metadata-only reader.
The v0.28.1 release binary includes all three changes; the per-revision
evidence above is intentional.

## User observations and remaining limits

On November 6 the user confirmed Q4 works well and Q8 regeneration succeeds,
reporting **about 45 tok/s generation and up to 1,550 tok/s prefill**, faster
than Q4 prefill in their workload. These are interactive observations, not
matched Q4/Q8 benchmarks. Rank 0 records Q8 responses of **12,875 tokens at
46.8 tok/s** (17:50:38 AWST) and **10,585 tokens at 45.4 tok/s** (18:02:08 AWST).

The user once saw `Error generating response body`; retry succeeded. Both
ranks remained alive and the inspected Gufo/proxy logs did not identify a
cause. No configuration change or stream fix was made. If it recurs, collect
client identity, exact time and client-side error details, then correlate
both ranks and the proxy. Do not label this a confirmed TP2 failure or a fixed bug.

Controlled timing compared fresh `uv-genai/main` **`78d8a4bf`** with the
numerical fix **`c1e4cc38`**, same compiler/settings/model/history. **58/66**
per-request phase comparisons were within 5% and 10 ms; **8 MTP** comparisons
remain inconclusive after a candidate repeat and unchanged-main controls.
All outputs and work/draft counts matched for those controls. Keep the slower
samples; no qualified speedup or confirmed timing regression is claimed. The
larger-prefill control changes output after the correctness fix and is not
comparable. [Timing record](docs/internal/models/qwen3.8-flash-next/BENCHMARKS.md#q8-regression-controls-november-6-2026).

Sparse attention passes its existing FP16 envelope against the independently
qualified reference. The extra full-model split probe retains a maximum logit
difference of **0.698152**; it is not a byte-exact sparse-prefill pass.
[Quality limits](docs/internal/models/qwen3.8-flash-next/QUALITY.md).

## TP2 invariants and future work

- **Same binary/revision/SHA on both hosts; one model process per GPU host.**
- Control protocol **23**, snapshot payload **v20**. Upgrade ranks together.
- `TpMirroredRunner::UsesComponentCache()` remains **false**.
- Draft subset/small head, prompt lookup copies and residual deferral stay
  single-host only. Rank 0 mirrors draft counts and execution shape.
- Mirrored in-pass checkpoint/rollback stays disabled; cancellation is between
  calls. The executor capability guard is deliberate and remains in Linux CI.
- Q8 cache identity includes `routed_projection=q8-paired-signed-v1`; old states
  miss and prefill again on both ranks.
- Collective order/count/byte size must match. Preserve TP2 half-width fused
  thresholds and YaRN group-2 support; see AGENTS and the merge checklist.

For the next upstream merge, use one upstream tag per branch/PR, audit TP2
hazards, format/build, deploy identical binaries, qualify generation/reuse and
get the requested user llama-swap check before release. Every published dated
tag needs written GitHub Release notes. Existing upstream version/changelog
files belong to the upstream release workflow.

Issue #1 (YaRN) is **closed**; NTK / `--rope-scale` are not implemented.
The remaining GLM issues are separate work and were not part of this release.
