# Upstream integrations, November 11, 2026

This record covers the sequential v0.32.0 and v0.33.0 integrations into Gufo-TP.
Unreleased upstream commits are excluded.

## Fixed validation scope

For each tag, resolve the merge on its own branch, validate, then merge its PR
before starting the next tag. Preserve the project README/AGENTS and native
host instructions while adopting the documentation layout semantically.

- Formatting, documentation, generated metadata and extension API policy.
- Native CPU PR contracts, including TP executor/control/snapshot contracts,
  scheduling, cache, sampling and structured-output tests.
- Release build and the affected Flash-Next routed/projection operators;
  snapshot-copy operators when the second tag changes them.
- Flash-Next Q4 and Q8 TP2 **MTP**, four sessions, context capacity 524288,
  static YaRN 2, matching binary SHA on both hosts. Actual generated text,
  drafts, rank logs, queue activity and cache work must pass.
- Per candidate: timing, seed/cache reuse and restart restoration, sampling
  defaults, tool streaming, Messages tools, reasoning budget, long-context,
  constrained output; Q4 also includes image inputs. No other model family.
- Timing controls use the immediately preceding main executable and the same
  harness/settings/history. Standard pp2048/tg128 and the existing TP2 timing
  controls run once for each model. A flag permits one focused
  main/candidate/main repeat for the affected history. Preserve all evidence;
  noisy timings remain inconclusive, and confirmed failures require fixes.

Stop after both PRs merge and the final report is written. Fixes rerun only
checks affected by the fix. There is no broader model matrix or benchmark sweep.
The user authorized both GPUs for this plan.

## v0.32.0

Tag c40862ff. The already-integrated v0.31.0 ancestry is recorded without a
source-tree change to make the release delta the merge base after squash.
Layer-yield callbacks and the newly extended decode-overlap path are gated to
single-host execution. TP2 retains mirrored snapshots, native RAM/disk restore,
forced draft counts, static YaRN and all existing single-host optimization gates.
TpMirroredRunner removes the new scheduling profile, preserving bounded token
chunks between mirrored calls; the model also rejects layer hooks under TP2.

Native PR checks pass 114/115 on the first execution; the new layer-yield
fixture lacked its explicit component-cache opt-in in the retained dual-cache
API. With that fixture adapted, the affected conformance check passes (115/115
covered in total). Release build and routed/projection GPU operators pass.
Formatting, docs, generated metadata, API policy and family boundaries pass.
Compiled source: `251757aa`; subsequent changes are test/docs only.

The first Q4 baseline overlapped CPU compilation and is retained as
non-qualifying timing evidence. Its isolated replacement is the timing control.
Q4 passes 196 and Q8 passes 166 TP2+MTP checks, including all declared suites,
actual drafts, session reuse/concurrency/cancellation, Q4 images and disk
restore after restarting both ranks. Both rank logs are clean; no forced stop.
Both deployed executables have SHA-256
`ed942b606cf8ee241d705cf806bcac150c8600fe1d45df1d3409cc5829311936`.

Timing is **inconclusive**, with all initial and follow-up captures retained.
Q4 initial 5.3–8.9% decode flags do not reproduce against both focused main
controls; main itself varies about 6–7%. Q8's initial decode flags are 5.7–8.2%.
Its focused candidate repeat has a large uncached-request outlier: standard
prefill 24.569 s versus 1.452/1.430 s on the surrounding main controls, and
decode 5.546 s versus 3.326/3.418 s. Cached decode remains near main.
The diagnostic replay on the unchanged candidate gives prefill 1.366 s and
decode 3.013 s, versus 1.383 s and 3.014 s on main. The large outlier did not
recur; its cause remains unresolved. No speedup or blanket timing pass is claimed.
Profiler attachment was unavailable because the native process lacked attach
support; the diagnostic replay is **unprofiled** evidence. The launcher now
waits for baseline process shutdown by PID state, including renamed binaries.

The [result index](models/qwen3.8-flash-next/artifacts/upstream-v0.32.0/results.json),
[functional evidence](models/qwen3.8-flash-next/artifacts/upstream-v0.32.0/functional-results.tar.gz),
[376 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.32.0/timing-observations.csv)
and [268 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.32.0/timing-comparisons.csv)
retain every result. Raw build/rank/diagnostic logs remain in
`artifacts/upstream-2026-11-11/v0.32.0/`.

## v0.33.0

Tag `77dff828`, integrated after [v0.32.0 PR #32](https://github.com/uv-genai/gufo-tp/pull/32)
(main `68faca6d`). The shared-expert calibration is single-host only: its
startup MoE calls are not mirrored and would add collectives during TP2 load.
Decode overlap and prefill layer callbacks retain their single-host gates.
The snapshot-copy registration-boundary repair and cache retention fixes are
integrated; native TP snapshots and restore remain available. README/AGENTS
retain project branding, native setup and the permanent 27B Q8 restriction.

Native PR checks pass 118/118; release build and all three selected GPU
operators (routed, projection, snapshot copy) pass. Both clang-format 21.1.8
and 23.1.1 pass, along with docs, metadata, family boundaries and API policy.
Two initializer layouts are adjusted to satisfy both formatter versions; the
v0.32.0 hosted format failure is corrected here.

TP2 runtime validation is in progress under the fixed scope above.
