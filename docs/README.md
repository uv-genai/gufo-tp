# Gufo documentation

Gufo is an open-source inference engine for AMD Strix Halo that serves text,
embedding, speech, image and video models over OpenAI-compatible APIs. These
pages explain how to install it, run models, and extend it with your own.

## Get started

For Gufo-TP's two-host deployment, start with the
[native build](../BUILD-LOCAL.md), [TP2 setup](../TP2-SETUP.md) and
[Flash-Next guide](models/qwen3.8-flash-next.md). The
[handoff](../handoff.md) records the deployed binary and validation scope.

1. [Install](install.md): container, Debian package, Nix, source or Windows.
2. [Models](models/README.md): what each official model does, the files to
   download and the speed to expect.
3. [Command line](cli.md): the `gufo` commands and their main options.
4. [Server](server.md): the HTTP API, clients, llama-swap and exposure.

## Run it well

- [Cache](cache.md): how Gufo reuses work across requests, and how to size it.
- [Troubleshooting](troubleshooting.md): diagnostics, logs and common failures.
- [Benchmarks](benchmarks.md): how the published speeds are measured.
- [Versions](versions.md): what a release promises and where it's published.

## Extend it

- [Extensions](extensions.md): add community models to your Gufo.
- [Writing an extension](writing-extensions.md): port a model of your own.
- [Extension API](extension-api.md): versions and the contracts a provider
  implements.

## About

- [Reference projects](reference-projects.md): the open-source engines Gufo
  builds on.

## Contribute

Developer documentation, design records and per-model evidence live in
[`internal/`](internal/development.md), in the repository only. Start with
[development](internal/development.md) and [testing](internal/testing.md).
