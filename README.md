# Advanced Database

Docker environments and examples for database coursework and experiments.

## Repository contents

- [`aquery/`](aquery/docker-x86-linux/README.md) - Build and run AQuery with Docker on x86-64 Linux.
- [`reprozip/`](reprozip/README.md) - Run ReproZip with Docker on x86-64 Linux.
- [`example/`](example/) — Example queries, datasets, and supporting scripts.

## Getting started

Choose a component above and follow its README.

## Verify on x86-64 Linux with Modal

```bash
modal run example/hw1_11/run_on_modal.py
modal run reprozip/run_on_modal.py
```

The first command compiles an AQuery program and executes the generated q with
KDB-X. The second traces, packs, inspects, unpacks, and reruns a Python program
with ReproZip.
