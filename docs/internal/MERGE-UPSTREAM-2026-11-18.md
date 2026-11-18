# Upstream integration, November 18, 2026

This record covers the v0.35.0 integration into Gufo-TP, stacked on the TP2
split draft-confidence fix. Unreleased upstream commits after tag `0260e116`
are excluded.

## Fixed validation scope

- Formatting with clang-format 21.1.8 (CI) and 23.1.1, documentation,
  generated metadata and extension API policy (`ext-api`).
- Native CPU PR contracts, including TP executor/control/snapshot contracts.
- Release build with `GUFO_ENABLE_TP2_RDMA=ON` on a host without XRT.
- Flash-Next Q4 and Q8 TP2 **MTP**, four sessions, context capacity 524288,
  static YaRN 2, matching binary SHA on both hosts. Actual generated text,
  drafts, rank logs and cache work must pass.
- Per candidate: timing, seed/cache reuse and restart restoration, sampling
  defaults, tool streaming, Messages tools, reasoning budget and separator,
  long-context, prefill scheduling beside a decoder, constrained output; Q4
  also includes image inputs. No other model family.
- Timing controls use the fix binary (this branch's parent) with the same
  harness, settings and history. A flag permits one focused
  main/candidate/main repeat. All evidence is retained; noisy timings remain
  inconclusive.

Stop after the PR merges and this record is written. There is no broader
model matrix or benchmark sweep.

## Merge

Tag `0260e116`, integrated after [v0.34.0 PR #36](https://github.com/uv-genai/gufo-tp/pull/36).
The already-integrated v0.34.0 ancestry is recorded first without a source-tree
change. Thirteen conflicts are resolved semantically:

- `src/ext/text.hpp`: the fork's non-pure component-cache hooks stay, so
  `TpMirroredRunner` can opt out; upstream's
  `CreateComponentCacheResourcesForSessions` is added with its fallback.
- `text_model_runner.cpp`: the fork's native/component lease split stays;
  upstream's rule that a runner without prefix reuse plans no captures and its
  cancelled-pass capture retention (`<` instead of `<=`) are adopted.
- `inference_backend.cpp`: upstream removes `TextPrefillPolicy`. The rank-1
  executor and mirrored-runner wrapping stay, with upstream's load-phase log;
  the TP handshake's prefill width becomes `kTpPrefillPassTokens`.
- `cmake/Checks.cmake`: both test lists, regenerated from model metadata.
- Nix package and scope: the TP2 RDMA variant keeps its options and also
  receives upstream's XRT and IRON inputs (not built here; Nix is not used on
  these hosts).
- Flash-Next `BENCHMARKS.md`, `EXPERIMENTS.md`, `QUALITY.md`,
  `tests/functional/README.md`: both sides, newest dated section first.
- `docs/internal/releasing.md`: the fork's Gufo-TP release section stays and
  the upstream policy body becomes upstream's current text.
- README and AGENTS are fork-owned. AGENTS gains upstream's Rust-components
  rule and its NPU design note; the prohibited-environment count stays 0.
  README keeps its quickstart and lists XRT as optional; the NPU device
  passthrough upstream added to its container example is not needed by TP2.

## TP2 hazard audit

| Upstream change | TP2 effect | Result |
| --- | --- | --- |
| Required scheduling profile, legacy budget removed (#1175) | `TpMirroredRunner` cleared the optional profile; that no longer compiles, and a default profile is rejected at load | **Fixed**: the mirrored descriptor declares `{pass_tokens = 512, max_layer_groups = 1}`, the former decode-active width, unsplit; no layer yields |
| Q4_K copy of the draft-head prefix (#1209) | Used only by the small-head subset path | Safe: `subset_ok` stays single-host; under TP2 the copy is built but never read |
| Compacted MTP inject rows (#1230) | Local buffer aliasing fix, same on both ranks | Safe: no collective change |
| Shared native transfer streams (#1195), frontier retention (#1183), disk recovery (#1194, #1196, #1205) | Component-cache paths | Safe: `UsesComponentCache()` stays false |
| No captures without prefix reuse (#1184), in-pass checkpoints (#1224) | Rank-0 pass planning | Safe: mirrored calls; `in_pass_checkpoint` and `prefill_rollback` stay false |
| Resume captured prefills first (#1181) | Rank-0 queue order | Safe: rank 1 follows mirrored calls |
| Reasoning separator after a closed block (#1210) | Rank-0 text output | Safe: no model call |
| Qwen family attention/SSM kernels (#1185, #1190) | Qwen3.8 27B only | Not linked by Flash-Next |
| XRT required at configure (#1186, #1227, #1229) | Hosts have no XRT | **Fork build change**: Linux builds without the NPU module when XRT is absent |

All existing gates remain: `UsesComponentCache()` false, `lookup_ok` and
`subset_ok` single-host, `defer_residual_` single-host, layer hooks and
decode-overlap calibration single-host. TP control protocol is 24 (from the
stacked fix) and snapshot payload 20.

## Validation

Native PR checks pass 134/134 (the stacked fix alone: 124/124). The release
build passes on these XRT-less hosts with the configure warning; the extension
API is 0.3.20 after upstream's 0.3 records. Two upstream callers of the
in-pass capture consumer (the Qwen3.8 27B prefill step and a component-cache
test) are adapted to the fork's `(index, native snapshot)` form; 27B is not
run on the GPU here. Both deployed executables are compiled from
`4bdc23c070385b4a1192103080811653f6e7d0fd`, SHA-256
`fef19e2d79ca2d7e74f273057b29e69b7ec39759dab70cba3f773666908f1e9b`; later
commits change tests and documentation only.

The candidate passes **394 TP2+MTP functional checks**: Q4 212, Q8 182,
including Q4 images, the new reasoning-separator suite, prefill scheduling
beside a decoder and disk restore after restarting both ranks. Both rank logs
are clean before every stop, no forced shutdown is needed and actual MTP
drafts execute (pp2048/tg128: Q4 78 proposed/52 accepted, Q8 75/53, identical
to the baseline). The first Q8 attempt failed in the harness before any
request reached the model: the served-model name did not match the retained
speed script. It is retained as `q8-harness-model-id-failure/`.

All 256 timing comparisons have identical output and work. The standard
pp2048/tg128 rates are, fix → candidate: Q4 prefill 1,498 → 1,501 tok/s,
decode 43.1 → 47.2 tok/s; Q8 prefill 1,436 → 1,470 tok/s, decode
36.0 → 42.0 tok/s. These are single observations, not a qualified speedup.

The initial comparisons flag Q8 long prefill (1,870.0 → 2,252.7 ms), warmup
and short-code-cached decode, Q8 `std0` decode and Q4 `std0` prefill. In the
focused fix/candidate/fix repeat none recurs (0 flags for each quantization):

| Phase | Fix | Candidate | Fix repeat | Candidate repeat | Fix control |
| --- | ---: | ---: | ---: | ---: | ---: |
| Q8 long prefill | 1,870.0 ms | 2,252.7 ms | 1,853.3 ms | 1,861.3 ms | 1,862.7 ms |
| Q8 warmup decode | 54.3 ms | 152.6 ms | 57.2 ms | 55.5 ms | 52.3 ms |
| Q8 short-code-cached decode | 1,342.2 ms | 1,448.3 ms | 1,323.7 ms | 1,334.7 ms | 1,337.8 ms |

The unchanged fix binary differs from itself beyond the limits in 7 Q4
phases (short-code prefill 178.4 → 228.9 ms). Timing is therefore
**inconclusive and unqualified**; no regression is confirmed and no speedup is
claimed.

A production-settings probe (two sessions, Q8; 12 greedy code prompts, six
concurrent greedy pairs, six seeded sampled prompts) alternates fix and
candidate twice. Every reply matches the fix (30/30 by full text in the
repeat), draft counts are identical and both rank logs stay clean. Single
greedy mean decode is 60.1 and 60.8 tok/s on the fix, 50.1 and 58.4 tok/s on
the candidate. The first candidate run's slow stretch (requests 5–9,
26.9–42.6 tok/s) does not recur; requests 1 and 4 are lower on the candidate
in both runs (−12.8%/−13.3% and −11.8%/−6.3% against the fix mean). These
are probe observations, not the qualified timing harness above: they stay
**inconclusive**, with [every request retained](models/qwen3.8-flash-next/artifacts/upstream-v0.35.0/probe-results.json).
Watch early greedy decode rates in the user llama-swap check.

The [result index](models/qwen3.8-flash-next/artifacts/upstream-v0.35.0/results.json),
[functional evidence](models/qwen3.8-flash-next/artifacts/upstream-v0.35.0/functional-results.tar.gz),
[320 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.35.0/timing-observations.csv)
and [256 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.35.0/timing-comparisons.csv)
retain every result. Comparison rows pair, per quantization: the initial fix
and candidate, the repeat fix and candidate, the repeat candidate and the
closing fix control, and the two unchanged fix runs. Raw build, rank and
harness logs remain in `artifacts/upstream-2026-11-18/`.
