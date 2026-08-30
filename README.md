# Advanced Database

Linux course material and reproducible environments for AQuery, KDB-X, and ReproZip.

## Repository contents

- [`course-materials/`](course-materials/README.md) - Student installation guides, lecture notes, and a worked ReproZip tutorial.
- [`aquery/`](aquery/docker-x86-linux/README.md) - Pinned x86-64 Linux Docker image and installation scripts for AQuery and KDB-X.
- [`reprozip/`](reprozip/README.md) - Pinned x86-64 Linux Docker image and ReproZip verification.
- [`example/simple_sales/`](example/simple_sales/README.md) - Small AQuery example with three rows and one filter.

## Getting started

Start with the [course-material index](course-materials/README.md).

## Verify on x86-64 Linux with Modal

```bash
modal run example/simple_sales/run_on_modal.py
modal run reprozip/run_on_modal.py
```

The first command compiles an AQuery program and executes the generated q with
KDB-X. The second traces, packs, inspects, unpacks, and reruns a Python program
with ReproZip.
