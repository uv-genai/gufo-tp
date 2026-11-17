# Upstream integration, November 17, 2026

This record covers the v0.34.0 integration into Gufo-TP. Unreleased upstream
commits after tag `2845939b` are excluded.

## Fixed validation scope

- Formatting with clang-format 21.1.8 (CI) and 23.1.1, documentation,
  generated metadata and extension API policy.
- Native CPU PR contracts, including TP executor/control/snapshot contracts.
- Release build with `GUFO_ENABLE_TP2_RDMA=ON`.
- Flash-Next Q4 and Q8 TP2 **MTP**, four sessions, context capacity 524288,
  static YaRN 2, matching binary SHA on both hosts. Actual generated text,
  drafts, rank logs and cache work must pass.
- Per candidate: timing, seed/cache reuse and restart restoration, sampling
  defaults, tool streaming, Messages tools, reasoning budget, long-context,
  constrained output; Q4 also includes image inputs. No other model family.
- Timing controls use the preceding main executable (`b325c75c`) and the same
  harness, settings and history. A flag permits one focused main/candidate/main
  repeat. All evidence is retained; noisy timings remain inconclusive.

Stop after the PR merges and this record is written. There is no broader
model matrix or benchmark sweep.

## Merge

Tag `2845939b`, integrated after [v0.33.0 PR #33](https://github.com/uv-genai/gufo-tp/pull/33).
The already-integrated v0.33.0 ancestry is recorded first without a source-tree
change. Eleven conflicts are resolved semantically:

- `engine.cpp`: upstream's `planned_greedy` backoff recovery is kept beside the
  TP2 forced draft count. It changes only rank-local policy state; rank 1 still
  takes rank 0's mirrored draft count.
- `text_generation_backend.hpp`: the deprecated `cache_shared_bytes` field is
  removed as upstream does; the fork's shared-prefix fields remain.
- `text_model_runner.cpp`, `Checks.cmake`, `ngram_test.cpp`: both sides kept.
- `text_cli_dispatch_test.cpp`: upstream's deprecated draft-flag behavior.
- Nix package, Rust license list and Flash-Next internal docs: both sides kept;
  upstream's move of the PR #877 controls into `QUALITY.md` is followed.

README keeps project branding; its prerequisites now list libopus instead of
libsndfile/libsoxr, matching the Rust audio decoder. libopus 1.6.1 is present
on both hosts. AGENTS.md has zero prohibited-environment matches.

## TP2 hazard audit

| Upstream change | TP2 effect | Result |
| --- | --- | --- |
| Fused batched FFN HC pair (#969) | Replaces a local combine/mix pair for ≤ 8 rows; no all-reduce added or removed | Safe: same geometry both ranks; `defer_residual_`/`moe_pending_` stay single-host |
| Q8 activation reuse from HC mixing (#958) | Local quantized rows, keyed by pointer/rows/width | Safe: no collective change |
| MTP backoff recovery (#912) | Rank-local `retry_tokens` | Safe: forced counts from rank 0 |
| Live-frontier alignment (#1154) | Dereferenced the component cache, which TP2 does not construct | **Fixed**: guarded; see below |
| Prompt-state admission (#1083, #1164) | Rank-0 admission before any model call | Inactive for Flash-Next |
| Disk cache admission/publication (#934, #1121) | Component cache path | TP2 keeps mirrored snapshots |
| Deprecated draft flags (#1124) | Flags ignored | TP2 launchers do not pass them |

All existing gates remain: `UsesComponentCache()` false, `lookup_ok` and
`subset_ok` single-host, `defer_residual_` single-host, layer yields and
decode-overlap calibration single-host. TP protocol stays 23 and snapshot
payload 20; no persisted layout changed.

### Frontier-alignment guard

Upstream v0.34.0 always constructs a component cache, so
`TextRunnerPool::AlignToLiveFrontier` dereferences it unconditionally. Gufo-TP
retains the pool cache for runners that opt out, which includes
`TpMirroredRunner`. The scheduler calls alignment for exact-incremental
runners with `cache_prompt` and no prompt context. Production TP2 serving
always passes a `TpRequestContext`, so the crash is latent there, but any
change to that wrapping would crash rank 0 on its first chat request. The
pool now returns false without a component cache, preserving the prompt as
tokenized. `TestPromptReuseWithoutComponentCacheKeepsPrompt` segfaults
without the guard and passes with it.

## Validation

Native PR checks pass 124/124. The release build passes; the extension API is
0.3.2 after upstream's 0.3 baseline. Both deployed executables are compiled
from `991ecf2a57dd5eb136fd8fd90e591ebcfa10781a`, SHA-256
`5503297f96e78a53beb52cd526ea47e2ec20c1bb172d4a2f005a809fca45ae61`.

The candidate passes **362 TP2+MTP functional checks**: Q4 196, Q8 166,
including all declared suites, Q4 images and disk restore after restarting
both ranks. Both rank logs are clean in every run, no forced shutdown is
needed and actual MTP drafts execute (pp2048/tg128: Q4 75 proposed/52
accepted, Q8 74/53, identical to main). The first Q4 attempt failed in the
harness before any candidate request because a renamed model ID did not match
the speed script; its baseline evidence is retained separately.

All 256 timing comparisons have identical output and work. The standard
pp2048/tg128 rates are, main → candidate: Q4 prefill 1,475 → 1,490 tok/s,
decode 38.3 → 42.9 tok/s; Q8 prefill 1,462 → 1,486 tok/s, decode
42.4 → 42.4 tok/s. These are single observations, not a qualified speedup.

The initial comparisons flag short-code prefill (Q4 187.6 → 222.4 ms, Q8
222.5 → 258.9 ms) and Q8 warmup decode (50.1 → 114.7 ms). In the focused
main/candidate/main repeat:

| Phase | Main repeat | Candidate | Main control |
| --- | ---: | ---: | ---: |
| Q4 short-code prefill | 198.1 ms | 188.9 ms | 168.1 ms |
| Q8 short-code prefill | 236.8 ms | 202.3 ms | 250.1 ms |
| Q8 warmup decode | 51.3 ms | 49.2 ms | 48.8 ms |

Q8 short-code and warmup do not reproduce. Q4 short-code remains flagged
against one of the two main controls; main itself spans 168–198 ms. The first
13-token request after load is flagged in the repeat (Q4 +5.8%, Q8 +8.4%) but
was faster on the candidate initially. The two unchanged main runs differ
beyond the limits in 7 Q8 and 1 Q4 phases. Timing is therefore
**inconclusive and unqualified**; no regression is confirmed and no speedup
is claimed. No additional GPU work is queued.

The [result index](models/qwen3.8-flash-next/artifacts/upstream-v0.34.0/results.json),
[functional evidence](models/qwen3.8-flash-next/artifacts/upstream-v0.34.0/functional-results.tar.gz),
[320 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.34.0/timing-observations.csv)
and [256 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.34.0/timing-comparisons.csv)
retain every result. Raw build, rank and harness logs remain in
`artifacts/upstream-2026-11-17/v0.34.0/`.
