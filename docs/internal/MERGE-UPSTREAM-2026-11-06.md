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


## v0.31.0

Upstream tag `be7bd3be` (`v0.31.0`), based on validated v0.30.0 PR #30
(`8d52f1c0`). Its upstream ancestry was recorded with no tree change before
merging this tag on its separate branch.

Provider sampling defaults, tool-dialect identity, reasoning markup and shared
options are integrated with the mirrored runner. TP control protocol 23 carries
the reasoning opener and whitespace mask and the exact automatic/reasoning/
content constraint state. Older peers are rejected; both hosts must upgrade.

The upstream component-only API transition is merged semantically: native
snapshot/fork and persistence interfaces remain for TP2, including the dual
serving lease, with public defaults for component-only providers. API 0.2.8
records that retained contract. Component providers explicitly opt into their
cache; TP2 continues to disable component restores and in-pass checkpoints.
Native RAM/disk caches and the mirrored prompt-context wrapper honor legal
prefill stops and preserve prefix identities. New tests cover these paths and
sampling agreement across the control channel, including opener token zero.

The equivalent upstream metadata-only GGUF fix is accepted with its clearer
missing-padding diagnostic, retaining both sets of regression tests. Q4 weight
links and native build/remote instructions were already current; README.md and
AGENTS.md remain project-owned. Shared kernel math and TP2 optimization gates
are retained. Snapshot payload 20 and the static YaRN cache identity remain.

Candidate executable `5b36be34283d77f7dfa61bbcff4beece8296b3e5`, SHA-256
`22e628c8f20aed0ee0067606242e63761fa6004d182a335e5fc949a76d77792b`.
Raw evidence: `artifacts/upstream-2026-11-06/v0.31.0/`.

- 10 focused native suites and 109/109 native PR contracts pass. Release build,
  clang-format 21/23, API policy, metadata generation, documentation and strict
  extension/link checks pass.
- GPU verification/sampling passes. Single-host Q4 AR/MTP image-state restoration
  compares logits and component bytes, rejects missing/changed image attachment,
  and passes restoration before future images.

[PR #31](https://github.com/uv-genai/gufo-tp/pull/31) integrates this tag.

- Q8 TP2 passes 332 AR/MTP checks, including 96 reasoning-budget cases,
  provider sampling defaults, tool streaming and Messages tools, constraints,
  long prefill, cache reuse, concurrency, cancellation and disk restore after
  restarting both ranks. Actual MTP drafts and clean rank logs are required.
- Q4 TP2 passes 392 AR/MTP checks, including the same controls plus 60 image
  checks. All four modes pass, using the byte-identical candidate on both
  hosts. No rank error or forced shutdown occurred.
- Single-host Flash-Next Q4 AR and MTP pass sampling defaults, tool streaming,
  reasoning budgets, long-context, cancellation, image-cache reuse and disk
  restart. Outputs and prefill/cache work match the v0.30.0 controls. MTP's
  3090 per-request/phase and lifecycle comparisons pass. AR retains 23 timing
  flags, principally concurrent snapshot/admission variation and three maximum
  inter-token-delay observations; these remain advisory/inconclusive.
- The completed Qwen27 Q4 AR/DFlash2 checks also pass functionally, with no
  output/work differences. Their initial timing reports retain 13 and 21 flags.
  The AR sampling-prefix main/candidate/main controls completed before shutdown:
  the final unchanged-main observation reproduces the short-prefill variation
  (288.7–311.0 ms on main versus 309.2–313.5 ms on the candidate for one case).
  The combined 1118 prefix-phase comparisons have 1078 within limits and 40
  inconclusive, with no confirmed slowdown. Concurrent requests exchange
  admission order and snapshot timing; no per-request flags are averaged away.

Validation closes with the evidence already collected. No further model runs
are queued. The user's scope is Flash-Next; **Qwen3.8 27B Q8 must never be run
again**, and 27B Q4 requires a specific justification. Its earlier Q8 baseline
hit the 900-second suite deadline, then completed with a 1800-second suite
deadline (120-second request deadlines and timing margins unchanged). The
candidate was stopped after sampling/tool checks and part of the reasoning
suite; Q8 AR/DFlash2 is not qualified. The additional Q4 DFlash2 timing prefix
was also stopped. Interrupted and incomplete reports are retained as such.

The [single-host result index](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/single-host-results.json),
[36119 recorded phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/single-host-observations.csv.gz),
[14598 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/single-host-comparisons.csv.gz)
and [completed Q4 AR prefix qualification](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/single-qwen27-q4-off-prefix-qualification.json.gz)
retain completed, failed-deadline and interrupted work. These totals are
evidence counts, not blanket pass counts. The remaining timing flags are
unqualified; no single-host speedup or all-model qualification is claimed.

Vision-enabled startup now hashes and uploads the projector before readiness.
In the Qwen27 Q4 AR warm restart, loader time changes from 1329 to 1824 ms;
the candidate records 424 ms for projector identity and 74 ms for upload.
The harness observes readiness at 1521.8 versus 2021.1 ms. These lifecycle
measurements include new preparation work and remain separate from matched
inference timings. The eager preparation is retained from upstream.

Timing compares the matching v0.30.0 executable `7f0d93f2`, with the same
ROCm toolchain, model files and ordered request histories. TP2 uses four
sessions, context capacity 524288 and static YaRN 2. Standard speed remains
canonical prose pp2048/tg128 at d0 (actual 2040 prompt tokens), greedy,
thinking off and one active client. Per-request/per-phase gates remain both
5% and 10 ms, with every initial and follow-up observation retained.

Q8 AR/MTP and Q4 MTP measured timings are within limits. Q4 AR initially
flags standard decode, 3579.2 → 3818.6 ms (+6.7%); its output and work counts
match. The focused main/candidate/main repeat gives 3592.9 / 3620.3 /
3580.1 ms, with every measured candidate phase within limits against both
controls. The initial slower capture did not reproduce and remains
advisory/inconclusive; no blanket timing pass or speedup is claimed.

The [352 phase observations](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/timing-observations.csv)
and [224 comparisons](models/qwen3.8-flash-next/artifacts/upstream-v0.31.0/timing-comparisons.csv)
retain initial runs, focused repeats and unchanged-main controls, including
setup and warmup. All measured output hashes and prompt, completion, cache,
prefill and draft counts match.

Hosted Linux CPU/repository checks and PR title/API policy pass for code head
`5b36be34` ([Linux run](https://github.com/uv-genai/gufo-tp/actions/runs/42228586718)).
Later changes are documentation and retained evidence only. The automatic
Windows package job fails on the existing POSIX TP control header
`arpa/inet.h`; its extension-contract job passes.

DeepSeek Flash 0731 weights are absent on both hosts; its AR/DSpark GPU paths
are not qualified by these checks. Windows remains outside this Linux task's
scope. The intermittent client stream error remains unreproduced, with no
claim that this integration fixes it.

Unreleased upstream main (`211dba49` at discovery) is excluded.
