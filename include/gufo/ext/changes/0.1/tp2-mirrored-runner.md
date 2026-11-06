# TP2 mirrored runner contracts

Add optional planned decode hooks and per-member forced draft counts to the text
runner, prompt-context encoding/decoding hooks, and continuation reuse checks.
Requests retain the original constraint JSON so a peer reconstructs the same
constraint. Defaults preserve single-host behavior. These source contracts keep
the Gufo-TP coordinator and worker on the same model-call sequence after the
extension migration; they do not promise a binary ABI.

The provider also owns TP transport creation. The host uses the public transport
control scope and passes it through runner options; device collectives and model
loading remain inside the provider. Providers without a transport factory reject
distributed loading.
