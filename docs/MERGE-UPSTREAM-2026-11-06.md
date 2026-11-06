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

## Subsequent tags

v0.30.0 (`f801b8ca`) and v0.31.0 (`be7bd3be`) were discovered but are not
part of this merge. Each follows on a separate branch and pull request after
validation. Unreleased upstream main (`211dba49` at discovery) is excluded.
