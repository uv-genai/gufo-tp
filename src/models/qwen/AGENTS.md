# Qwen3.8-27B model directory

This directory owns the 27B source extension: target inference, native MTP,
DFlash2 and hidden-state encoding. `extension.json` declares the provider;
`extension.cmake` registers `gufo_qwen` and `gufo_qwen_hip`.
Follow the model restrictions in the root AGENTS.md before any model launch.

Shared Qwen code is not here. The tokenizer, chat template, control tokens,
GGUF configuration extraction, shared HIP operators, RoPE layout and vision
stack live in [`src/families/qwen/`](../../families/qwen/README.md), and their
rules — including the control-token catalogue and the Python mirror — are in
[`src/families/qwen/AGENTS.md`](../../families/qwen/AGENTS.md).

Model rules:

- Depend on family libraries through the libraries named in
  `src/models/qwen/extension.cmake`; do not reach into another model directory.
- Keep kernel per-source compile options bound to this target
  (`TARGET_DIRECTORY gufo_qwen_hip`); a moved kernel must keep them and its
  production code objects must stay identical.
- Run the model quality runners before changing arithmetic, layouts or cache
  boundaries.
