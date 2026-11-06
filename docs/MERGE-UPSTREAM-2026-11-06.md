# Upstream integrations, November 6, 2026

## v0.29.0

Upstream tag: `883f67b6` (`v0.29.0`). Development base: `426496a4` on
`uv-genai/main`. The already integrated v0.28.1 ancestry was recorded without
changing the tree before merging the next tag.

The source-extension migration moves Flash-Next's text runner into its model
extension. TP transport creation now belongs to that provider; the host uses a
public transport control scope and retains the mirrored runner/executor. The
standalone TP session and snapshot path remain available while single-host
serving uses component adapters. Strict extension ownership, include and link
boundaries pass.

TP2 continues to disable draft subsets, prompt lookup copies, deferred
residuals, rank-local component-cache restore and dynamic YaRN re-rotation.
Both ranks retain static YaRN, forced draft counts and split-head geometry.
The corrected paired-Q8 projection and metadata-only GGUF reader are preserved.
Control protocol 22 rejects older peers; snapshot payload 20 and the static
position-policy identity invalidate incompatible persisted states.

The capability audit caught upstream's vision and prefill-alignment fields.
The mirrored RAM and disk caches now reject unaligned snapshots for longer
prompts, retaining aligned fallbacks and exact-prompt retries. New regression
tests failed before the selection fix and pass afterward.

README.md and AGENTS.md were merged semantically. Branding, native host setup,
remote policy, current model links and release evidence remain project-owned.
The native TP package and development shell remain available. A redundant
conditional parenthesis keeps formatting compatible with clang-format 21/23.

[PR #29](https://github.com/uv-genai/gufo-tp/pull/29) integrates this tag.
Validation records are under `artifacts/upstream-2026-11-06/v0.29.0/`.

| Compiled revision / scope | Result |
| --- | --- |
| Initial `78f96d6c`, native PR suite | 107/107 tests; release build, format, public API inventory, generated metadata, documentation and strict extension boundaries pass |
| Initial `78f96d6c`, GPU numerical suites | 8/8: HC mix/route, GDN, attention, projection, routed WMMA, snapshot copy and verification sampling; existing tolerances |
| Initial `78f96d6c`, Q8 TP2 | 190 AR/MTP functional checks plus standard speed captures |
| Final cache repair `3ea5054d`, native tests | RAM and disk alignment regressions reproduce before the fix; four affected cache/runner/TP executor suites pass afterward |
| Final `3ea5054d`, Q8 TP2 follow-up | 94 AR/MTP cache, continuation, constrained-output and disk-restart checks plus speed captures |
| Final `3ea5054d`, Q4 TP2 | 250 AR/MTP functional checks, including 60 image checks and 96 reasoning-budget checks, plus speed captures |
| CI import policy `b406bba1` | 20 API-policy tests; the actual PR-base diff accepts first-time API introduction while requiring the label and active-series record |

Both hosts run the same final executable, SHA-256
`43be578145df68a7cf15a7e391910269fdc9763fbde3d8a251a122970f549da4`.
Its full compiled revision is `3ea5054d6256266d9e48199e0665897019a5859f`;
later commits change CI policy and documentation only. GPU operators are
unchanged by the final cache fix, so their earlier numerical evidence applies.

All pairs use four sessions, context capacity 524288, static YaRN factor 2,
matching Q4/Q8 files and the Q8 MTP head when enabled. The checks assert
generated text, long prefill, short code, repeated-prefix reuse, concurrent
requests, cancellation, actual MTP draft activity and disk restore work. Both
rank logs are clean before controlled shutdown. This is Linux TP2
qualification, not a full-depth context or every-model GPU qualification.
The earlier intermittent client stream error remains unreproduced; this merge
does not claim to fix it.

Timing uses unchanged main's `85ae8ce2` executable (code matches development
base; later main commits are documentation), the same ROCm toolchain, model
files, four sessions, context 524288 and static YaRN. Gates remain per request
and phase: an increase must exceed both 5% and 10 ms to flag. No averages or
wider tolerances are used. Standard speed uses canonical prose pp2048/tg128
at d0, actual prompt 2040 tokens, greedy, thinking off and one active client.

The [608 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.29.0/timing-observations.csv)
and [544 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.29.0/timing-comparisons.csv)
retain initial runs, cache-fix follow-ups, alternating repeats and unchanged-main
controls, including setup/warmup requests. Output hashes and prompt, cache,
completion and draft counts accompany the timings. The standard measured request
is `standard-pp2040-tg128`; its preceding calibration/ready requests are setup.
All measured follow-up output/work comparisons match.

- **Q4:** initial MTP measured requests are within the regression threshold.
  AR cached-long decode initially flags, 2552.4 → 2714.8 ms (+6.4%). The focused
  main/candidate/main sequence gives 2545.5 / 2525.1 / 2555.2 ms; its measured
  candidate phases are within threshold against both controls. The initial
  slower capture is retained and did not reproduce.
- **Q8 AR:** short prefill initially flags, including 201.0 → 270.1 ms on the
  final cache-fix run. A focused main/candidate/main sequence gives
  237.7 / 221.6 / 256.1 ms. Unchanged main itself flags (+7.8%); the candidate
  repeat is within threshold against both main controls. The original slower
  sample remains advisory/inconclusive.
- **Q8 MTP:** initial/repeated candidate decode and short-prefill flags coexist
  with drift on unchanged main. For example, repeated long decode is
  2120.8 / 2262.2 / 2244.7 ms across main/candidate/main; main itself moves
  +5.8%. Final candidate cache-follow-up measured phases are within threshold
  against that unchanged-main control. Earlier flags remain visibly
  advisory/inconclusive; no speedup or blanket timing pass is claimed.

Native validation is complete. Hosted PR title/API policy passed. The automatic
Windows package job fails compiling the POSIX TP control transport
(`arpa/inet.h`); Windows was explicitly excluded from this work. Its extension
contract job passed. Hosted Linux CPU/repository checks passed for code head `b406bba1`
([run](https://github.com/uv-genai/gufo-tp/actions/runs/42216446033)).
Subsequent commits update documentation only; the native suite above is
separate evidence.

## v0.30.0

Upstream tag: `f801b8ca` (`v0.30.0`). Development base: `9e12cfb2`,
PR #29's validated v0.29.0 integration. Its upstream ancestry was recorded
without changing the tree before merging this tag on a separate branch.

Single-host component serving gains multiple checkpoints within a prefill
pass, with shared checkpoint windows in the attention and GDN kernels.
TP2 retains mirrored native RAM/disk snapshots and explicitly rejects in-pass
checkpoint entry points. Its paired prefill, rank-local head geometry,
static YaRN, forced draft counts and single-host-only optimization gates remain.
Control protocol 22 and snapshot payload 20 are unchanged.

Upstream's component-only host cleanup was integrated semantically: the native
TP continuation cache, persistence, public metrics and runner contracts remain.
The upstream component tests and retained native snapshot tests run separately.
Those native tests exposed an attempted second reservation of an already
reserved snapshot; the merge now re-reserves only component captures.
README.md and AGENTS.md retain project ownership and native host instructions.

Validation uses executable `7f0d93f232ae2337e851706bc8479ed5db9563dc`, SHA-256
`9ad8a5a3b4d81a53f2eb6bed136e97a2f894da661c1cd45bd70826bcdee54f7a`.
Both hosts receive this exact binary. Raw records are under
`artifacts/upstream-2026-11-06/v0.30.0/`.

- Native PR contracts: 109/109 pass; release build, formatting, generated
  metadata, API 0.1.21 policy, documentation, strict extension boundaries and
  target link graphs pass.
- GPU operators: GDN, attention and projection pass with existing tolerances.
- Single-host Q4 checkpoint numerical checks: all eight AR/MTP comparisons
  pass, including multiple boundaries and the device-exhaustion fallback,
  against independently split passes.

- Two-host Q8: 94 AR/MTP functional checks pass. Two-host Q4: 154 AR/MTP
  checks pass, including 60 image checks. Both modes cover cache reuse,
  concurrency, cancellation, long prefill, constrained output and disk restart.
  All rank logs are clean before controlled shutdown. Actual MTP drafts are
  verified, using four sessions, context capacity 524288 and static YaRN 2.

[PR #30](https://github.com/uv-genai/gufo-tp/pull/30) integrates this tag.
The matching v0.29.0 executable `3ea5054d` is the timing baseline; no unrelated
correctness sweep is repeated on main. Same toolchain, models and settings,
per-request/per-phase thresholds of both 5% and 10 ms, and standard d0
pp2048/tg128 (actual 2040 prompt tokens) are retained.

Q8 MTP and Q4 AR initial measured timings are within limits. Q8 AR initially
flags standard decode, 3919.0 → 4960.6 ms (+26.6%), and other phases. The
focused main/candidate/main sequence gives 3949.5 / 3978.4 / 4337.8 ms;
unchanged main itself moves +9.8%. Candidate repeat measured phases are within
limits against both controls. The initial slower capture remains retained and
advisory/inconclusive, without a blanket timing pass or speedup claim.

Q4 MTP initially flags standard decode, 2716.5 → 3019.5 ms (+11.2%),
and several other phases. The main/candidate/main repeat gives
2761.0 / 2703.3 / 2782.3 ms, with every measured candidate phase within limits
against both controls. The initial slowdown did not reproduce and remains in
the record; no margins were widened.

The [448 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.30.0/timing-observations.csv)
and [320 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.30.0/timing-comparisons.csv)
include initial runs, repeats, unchanged-main controls and setup/calibration
requests. Measured output hashes and prompt/cache/completion/draft work match.
The automatic Windows package path remains outside this Linux qualification;
the retained POSIX TP transport has not been ported. Hosted Linux and API/title
results are linked from the pull request. Both GPUs are unloaded after testing.


## Subsequent tags

v0.31.0 (`be7bd3be`) follows on its own branch and pull request after validation.
Unreleased upstream main (`211dba49` at discovery) is excluded.
