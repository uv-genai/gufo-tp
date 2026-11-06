# LIVE HANDOFF — gufo-tp fork (Gufo-TP)

**Canonical path:** `handoff.md` in **this repository** (`/home/ugo/projects/gufo/handoff.md`).
**New sessions read this first** (also see `~/gufo-merge-handoff/handoff.md` only as a
redirect until that copy is removed).
**When state changes** (merge, tag, push, script/config change, incident): **replace
or edit this file in full** — do not leave stale tips, shas, or “untested” claims.

Last updated: **2026-11-06** (session: **review fixes #21–#24 validated on `codex/fix-tp2-review-findings`; CPU/PR, GPU operator and AR/MTP serving checks PASS; timing observations retained below** — baseline recheck in §2. Project is **Gufo-TP**; repo `uv-genai/gufo-tp`).

---

## 0. Read next (in order)

1. **This file** (`handoff.md` at the repo root)
2. Repo `AGENTS.md` (build, remotes, TP2 hazards, **nix count must be 0**)
3. `docs/MERGE-CHECKLIST.md` (merge + TP2 runtime process)
4. `docs/models/qwen3.8-flash-next/TP2.md` (collective rules)
5. `docs/MERGE-UPSTREAM-2026-10-24.md` (v0.16→v0.23 series write-up)

Historical dated handoffs in `~/gufo-merge-handoff/HANDOFF-*.md` are **archive only**.

---

## 1. Repo & remotes

| | |
| --- | --- |
| Tree | `/home/ugo/projects/gufo` |
| Development | **`main` → `uv-genai/main`**; review branch **`codex/fix-tp2-review-findings`**, validated before PR merge |
| Push | **`uv-genai` only** → https://github.com/uv-genai/gufo-tp.git |
| Upstream | `origin` → gufo-org/gufo; local track **`gufo-org`** — **never push** |
| Review PR | [#25](https://github.com/uv-genai/gufo-tp/pull/25) |
| Review code | **`a40b1616`** contains the request-control/Q8 fixes and cache epoch; numerical kernel source **`c1e4cc38`**; main control is **`78d8a4bf`**; previous release code **`2a7c0262`** = **`tp2-rdma-merge-v0.28.1-2026-11-04`** (PR #20 squash) |
| Upstream merged through | **v0.28.1** (`12effe36`); README tracks through v0.28.1; released |
| v0.27.0 tag | `tp2-rdma-merge-v0.27.0-2026-10-31` — https://github.com/uv-genai/gufo-tp/releases/tag/tp2-rdma-merge-v0.27.0-2026-10-31 |
| Release notes | **https://github.com/uv-genai/gufo-tp/releases/tag/tp2-rdma-merge-v0.28.1-2026-11-04** (v0.27.0: …/tp2-rdma-merge-v0.27.0-2026-10-31) |
| Repo rename | 2026-10-29: `uv-genai/gufo` → **`uv-genai/gufo-tp`**; project is **Gufo-TP** (binary/CLI stays `gufo`) |

**Non-negotiables:** `grep -ci nix AGENTS.md` → **0**; never run that package
manager; Conventional Commits; ask before any GPU launch.
**Every future tag must also get a GitHub Release with written notes** (user
directive 2026-10-29) so the tag row shows the notes link.

---

## 2. Binary & tested configuration

| | |
| --- | --- |
| Path | `build/release/gufo` on **both** hosts |
| sha256 | **`37feeaadddc1e870eb48427e8239c445106ec8e203363731de2c1642c5d909f1`** — validated on both hosts |
| Built from | **`a40b1616`** (request controls, paired Q8 expert fix and persistence numerical epoch); original v0.28.1 binary (`42aded09…`, source `2a7c0262`) retained on both hosts at `artifacts/tp2-review-fixes-2026-11-06/gufo-main` |
| TP2 smoke | **2026-11-04 PASS 10/10** on both hosts, sha `42aded09…` matched; `/ready` 200; PONG, 3481-tok long, short eBPF NL content asserts, 5× session, 2× agent prefix; logs free of `tp_pair_lost`/mismatch/status5; only expected `q8_0_expanded` WARN (168 tensors) |
| Review-fix validation | **2026-11-06 PASS 171 functional checks**, Q8 TP2 AR/MTP, sessions 2, context 524288, YaRN 2; actual MTP drafts, cache bypass/RAM/disk restart, budgeted reasoning and constraints. Release SHA above matches on both hosts. Evidence `artifacts/tp2-review-fixes-2026-11-06/validation-3/`. GPU operators **3/3**, CPU PR checks **80/80**. Timing remains advisory as detailed in §5. |
| Pre-fix GPU recheck | **2026-11-06 PASS 22/22**, same existing binary and matching launchers on both hosts. Q8 TP2 + MTP, sessions **2**, context **524288**, YaRN **2.0**, HTTP **8322**. PONG; **3877-token** prompt across 3 prefill chunks; short eBPF content assertions; 5 session-reuse requests; exact greedy agent replay with **85 cached tokens**; 3 concurrent requests with **2 active / 1 queued**; 9 tool/JSON/streaming/mixed-concurrency cases. Metrics: **811 proposed / 720 accepted MTP draft tokens**. `/ready` remained 200; both logs free of collective/peer/error failures; only expected `q8_0_expanded` WARN. Both owned ranks stopped; both GPUs idle and test/bootstrap/control ports released. |
| Recheck evidence | **`artifacts/tp2-mtp-smoke-2026-11-06-134039/`**: metadata and both-host hashes, reproducible `run_smoke.py`, `report.json`, `constraints/report.json`, full rank logs, concurrency samples, metrics, cleanup record. Greedy, thinking off, disk cache off; configured context capacity is not a full-depth context qualification. This smoke predates the review fixes and does not qualify their reasoning or persistence controls. |
| v0.26.0 smoke | **2026-10-29 PASS** on both hosts, sha `7b9c4e48…` matched; `/ready` 200; 10/10 requests (PONG, 3481-tok long, short eBPF NL w/ content asserts, 5× session, 2× agent prefix); logs free of `tp_pair_lost`/mismatch/status5; thinking off via `chat_template_kwargs` for asserts |
| User llama-swap (Q8-tp2) | **2026-10-29 PASS** (v0.26.0); **2026-10-31 PASS** (v0.27.0): “works well”; **2026-11-04 PASS** (v0.28.1): prose eBPF tutorial prompt 9,877 / gen 379, prefill **947.91 t/s**, gen **51.79 t/s**, tutorial 50% longer than previous — speed and quality both good |
| Three-way spot bench | **2026-10-29** sha `7b9c4e48…`; artifact `artifacts/three-way-2026-10-29.json`; driver `tools/bench/three_way_q4_q8.py` **on strix-halo-1**; REPS medians, unique salts, `cached=0`, `--think off`, ctx 32768 |
| Released | **`tp2-rdma-merge-v0.28.1-2026-11-04`** (this tag) plus `v0.27.0-2026-10-31` and `v0.26.0-2026-10-29` on uv-genai with GitHub Release notes; **not** pushed to origin |
| Configure | three host flags in `AGENTS.md` (HIP compiler + `-include format`) |

**TP2 serve defaults** (all four `tools/tp2/rank{0,1}-{q4,q8}.sh`):

```text
--sessions 2
--context 524288
--enable-yarn
```

- YaRN factor = **524288 / 262144 = 2.0** (`event=yarn factor=2.000000` at load).
- **Both ranks must pass identical `--context` / `--enable-yarn` / `--sessions`** or
  handshake fails (`context X here, Y on the peer`).
- **Scripts live in a separate checkout on each host.** After editing
  `tools/tp2/*.sh` on this machine, **scp or git-pull them onto `strix-halo-1`**
  (rank0 runs from strix-halo-1’s tree). Miss this → config mismatch.

---

### 2b. Three-way spot numbers (2026-10-29, medians of 5)

Driver: `python3 tools/bench/three_way_q4_q8.py` **on strix-halo-1**.
Modes AR + MTP; depths short/medium/long; C=4 aggregate in the artifact JSON.

| Depth | Metric | onehost Q4 | Q4 TP2 | Q8 TP2 |
| --- | --- | ---: | ---: | ---: |
| short ~200 | pp AR / MTP | 864 / 859 | 609 / 613 | 550 / 573 |
| short | tg AR / MTP | 27.6 / 43.4 | 33.4 / 46.9 | 30.9 / 45.2 |
| medium ~2k | pp AR / MTP | 1784 / 1726 | 1822 / 1693 | 1592 / 1527 |
| medium | tg AR / MTP | 27.2 / 41.9 | **32.6 / 46.8** | 29.8 / 41.1 |
| long ~8k | pp AR / MTP | 1836 / 1760 | 1895 / 1762 | 1684 / 1639 |
| long | tg AR / MTP | 27.4 / 42.4 | **32.5 / 46.3** | 30.1 / 40.7 |
| C=4 short | agg tok/s AR / MTP | 60.2 / 81.4 | 70.1 / 75.1 | 54.0 / 62.7 |

Short-depth `n` is 1–4 where greedy hit EOS before `max_tokens` (rejected).
`cached=0` on every retained sample. Q8 does not fit one host (no onehost column).


## 3. Hosts & launch

| Role | Host | Notes |
| --- | --- | --- |
| rank0 (HTTP) | **strix-halo-1** `192.168.1.22` | llama-swap + `tools/llama-swap/tp2.sh` |
| rank1 (worker) | **strix-halo-2** (this box) | started by ssh from rank0 |

- Bootstrap `18515` / control `18516` / token `92ffa404804d336980d95f224d6bd678`
- Q8 llama-swap model id: **`gufo-qwen3.8-flash-next-tp2-q8`** → port **5809** (not 8080)
- Start: `tools/llama-swap/tp2.sh run PORT q4|q8` on strix-halo-1 (or swap `run`)
- Stop: `tools/llama-swap/tp2.sh stop`
- Logs: `~/gufo-tp2-swap.log` (rank0), `~/tp2-rank1-swap.log` (rank1), `~/tp2-swap.log`
- **One `gufo` per GPU host.** Same sha both ranks before interpreting any hang.

---

## 4. TP2 gates (must stay true)

| Gate | Where |
| --- | --- |
| `lookup_ok = TpWorldSize()==1` | `engine.cpp` (`lookup_cap`) |
| `subset_ok = allow_subset && TpWorldSize()==1` | `engine.cpp` (`draft_subset`) |
| Forced draft width from rank 0 | `request.drafts` / `batch_drafts` |
| `defer_residual_` only if `tp_world_size()==1` | `executor.cpp` |
| `UsesComponentCache()` **false** | `tp_executor.cpp` |
| Wide-prefill fused paths need **`n ≥ 1024`** under TP2 half-width | `executor.cpp` / `kernels.hip.cpp` |
| YaRN fused attention: **group-4 AND group-2** (26 tiles on TP2) | `kernels.hip.cpp` `AttentionF16Gemm` |

Prompt lookup type: **`speculative::PromptLookup<>`** (moved in v0.22), payload v18.

---

## 5. Known failures (do not regress)

**Review scope (user directive, 2026-11-06): Windows is out of scope.**

**Validated review fixes (2026-11-06):**

- [#21](https://github.com/uv-genai/gufo-tp/issues/21): protocol v21 mirrors reasoning budgets, forced/early end tokens, prompt state and UTF-8 masks; the wrapper forwards model reasoning metadata.
- [#22](https://github.com/uv-genai/gufo-tp/issues/22): every TP request bridge preserves `cache_persist`; raw Completions also preserves `cache_prompt`.
- [#23](https://github.com/uv-genai/gufo-tp/issues/23): restored the relevant executor test, audited all 12 capabilities and added Linux PR coverage. Mirrored in-pass rollback remains unsupported.
- [#24](https://github.com/uv-genai/gufo-tp/issues/24): larger Q8 prefills exposed a pre-existing paired expert bug. Layer 0's MoE input matched but output differed; the independent operator test found zero paired gate/up results. The kernel now decodes signed Q8 code halves with their scale and supports 64-element K stages. Byte-exact TP/full-width route tests and numerical/operator checks pass.

CPU regressions **2/2**, Linux PR checks **80/80**, GPU attention/projection/routed
operator suites **3/3**, formatting **723 C++ files with clang-format 21 and 23** and documentation links
pass. Candidate serving runs and all failed investigations are retained under
`artifacts/tp2-review-fixes-2026-11-06/`. `validation-3/summary.json` passes:
**96** reasoning-budget checks (48 each in AR/MTP), **18** long-context and
cancellation checks, **48** cache checks including both-rank disk restart, and
**9** MTP constraint/tool/concurrency checks. Chat and raw buffered/SSE return
exact `BETA` through bypass, RAM replay and disk restore; private requests do
not persist. Actual drafts are present in MTP and absent in AR. Matched timing
controls use a fresh `uv-genai/main` (`78d8a4bf`) build with identical compiler,
dependencies and flags: `matched-timing-1/` and `matched-timing-followup-1/`.
All compared output hashes, prompt/cache work and draft counts match. **58/66**
phase comparisons are within 5%/10 ms; **8 MTP** comparisons remain inconclusive
and advisory after a candidate repeat and unchanged-main controls. No qualified
speed improvement or confirmed regression is claimed. The earlier large-prefill
control changes output with the Q8 correctness fix and is timing-incomparable.
Every initial and follow-up result remains retained.

The attention/projection/routed suites all pass. Sparse attention keeps its
existing FP16 envelope against the independently qualified reference; the
extra full-model split probe has nonzero logit differences (max 0.698152).
See `docs/models/qwen3.8-flash-next/QUALITY.md` for that retained diagnostic
and the added grouped/single-query operator check. This is not a claim of
full-model byte-identical sparse logits across chunk layouts. Both owned ranks
are stopped after validation; test ports are released.
The final identity epoch rejects disk states computed by the old Q8 projection
path. The previous main binary primes a real two-rank cache; the upgraded
binary must miss and prefill all tokens. This and fresh AR/MTP seed/restart
coverage pass in `final-cache-validation-1/`: **50** cache/upgrade checks and
**9** MTP constraint checks, including the old-binary primer. The final release
source is `a40b1616`, with the SHA above on both hosts. Linux PR checks pass
**80/80** again. The four pre-existing format differences found by hosted CI
are now compatible with clang-format **21 and 23**, both **723/723**.

The user reports a completed Q4 re-download; current validation uses Q8.

**Executor-test relevance audit (2026-11-06): keep the test.** It runs the current
production scheduler, pool, TCP channel, `TpMirroredRunner` and `TpExecutor` with
a deterministic CPU model. Production still instantiates both executor classes.
Commit `d1235f23` (2026-10-07, the test's last change) deliberately added the
compile-time capability guard. `partial_prefill_retention` (2026-10-13) and
`prefill_rollback` (2026-10-21) subsequently expanded the interface without a
corresponding TP2-test audit. The test remains registered as `cpu;tp2` in CTest;
there is no history of it being added to `cmake/Checks.cmake`. Its divergence,
rejected-cache dependency, cancellation and disk-restart checks add coverage
beyond the passing GPU smoke. Repair requires auditing the new capabilities
and restoring the test/build integration. The branch now restores this test and its cache dependencies, adds it to Linux PR checks, and explicitly disables in-pass rollback on the mirrored wrapper.

| Symptom | Cause | Fix / policy |
| --- | --- | --- |
| Large Q8 prefill changes replies across chunk boundaries | Paired Q8 expert kernel used zero scales and nibble decoding | Signed-byte paired decode + K64 stages (`c1e4cc38`), issue #24 |
| `identity or size mismatch` | Rank skipped split-argmax or lookup cycle | Draft-subset + lookup single-host only |
| Session reuse hang | Component-cache restore rank-0 only | `UsesComponentCache()==false` |
| Short NL “scrambled text” / empty content | Wide-prefill fused `n>8` but TP2 needs `n≥1024` | `bb383a36` thresholds |
| `fused attention projection failed` under YaRN | YaRN launch required `tiles%4==0`; TP2 is 26 tiles | `80e3a7c4` group-2 yarn launch |
| Handshake `context/sessions mismatch` | Rank scripts stale on one host | Sync **all four** rank scripts on **both** hosts |
| RDMA status 5 first prefill | Often link/Thunderbolt after desync | Fix desync first; don’t loop restarts |
| Hang after v0.26 side-stream MoE/DeltaNet | Side-stream work must `JoinSide` before AR/epilogue; TP2 `reduce`/`AllReduce` path kept | Merged `Moe` keeps `!reduce \|\| AllReduce`; `UsesComponentCache` still false |

---

## 6. Process (each new upstream release)

1. `git fetch origin`; create branch **`merge-upstream-vX.Y.Z`**; merge **one tag**
   per `docs/MERGE-CHECKLIST.md`.
2. Resolve conflicts **keeping TP2/MTP gates**; README/AGENTS/SERVER docs: **semantic
   merge** (fork owns them — integrate upstream additions, keep Gufo-TP branding);
   AGENTS nix count **0**.
3. Format (`tools/ci/check-format.py`) + release build (host flags).
4. Ship **same sha** to strix-halo-1; no leftover `gufo` (pre-flight: ports 18515/16,
   `amd-smi` processes, both hosts `pgrep -ax gufo`).
5. Smoke on branch: PONG, >1024-token prompt, short NL (eBPF-style content assert),
   ≥5 @ sessions, agent-style, logs free of mismatch/status5/`tp_pair_lost`.
6. **User llama-swap** validation (Q8-tp2).
7. **PR into `main`** (squash merge; title `chore: merge upstream vX.Y.Z into main`).
8. Tag `tp2-rdma-merge-vX.Y.Z-<YYYY-MM-DD>` on merged `main`; push **uv-genai only**;
   **GitHub Release with notes** (required).

Dated tags: v0.16.0-2026-10-17 … **v0.28.1-2026-11-04** (Release notes linked). Next: next upstream. **Each new tag: push uv-genai + create GitHub Release with notes.**

---

## 7. Docs owned in this repo (keep current)

| Path | Purpose |
| --- | --- |
| `README.md` | fork overview; tracks upstream **through v0.28.1** (Gufo-TP branding; no nix section; Windows build note kept; TP2 table still 2026-10-14 numbers) |
| `AGENTS.md` | build, remotes, **TP2 hazard table** |
| `docs/MERGE-CHECKLIST.md` | merge + runtime checklist |
| `docs/MERGE-UPSTREAM-2026-10-24.md` | series write-up |
| `docs/models/qwen3.8-flash-next/TP2.md` | collective rules |
| `docs/SERVER.md` / `docs/CLI.md` | `--enable-yarn`, context > 262144 |

External: **uv-genai/gufo-tp issue #1** — comment on YaRN implementation
(v0.21.0+); still open (NTK / `--rope-scale` API not implemented).

---

## 8. How this session should use the file

1. **Start of session:** read this file; do not rely on old `SESSION-PROMPT-*` or
   `HANDOFF-2026-*.md` under `~/gufo-merge-handoff/` unless explicitly asked for
   history.
2. **End of session / after any of the above changes:** rewrite or edit
   **this** file so the next agent can cold-start without guessing.
3. Prefer one canonical path: **`handoff.md` at the repo root** (this file).
