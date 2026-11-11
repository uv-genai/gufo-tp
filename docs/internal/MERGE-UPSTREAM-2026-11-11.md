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

Validation and PR identity will be recorded after the checks complete.
