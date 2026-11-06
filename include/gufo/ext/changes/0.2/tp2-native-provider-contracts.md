# Retained native TP continuation and provider contracts

Gufo-TP retains `ContinuationSnapshot`, `TextRunnerSnapshot`, native snapshot
and fork capabilities, persistence descriptors and the `TextModelRunner`
state/snapshot serialization hooks across the upstream 0.2 transition.
`CreateState` has a default which throws for component-only providers.
Component resource/binding hooks retain defaults for native providers;
component runners explicitly return true from `UsesComponentCache`.
The two-argument in-pass consumer and its single-boundary compatibility
bridge remain available, while TP2 itself rejects in-pass capture.

The mirrored runner forwards provider tool-dialect identity, reasoning
markup, sampling defaults and prompt-context legal stops/prefix identities.
Both native cache tiers honor indivisible input boundaries. TP control
protocol 23 carries automatic reasoning state, reasoning openers and blank
masks; peers on previous protocol revisions are rejected. Native snapshots
remain model-owned and component restores remain disabled for TP2.
