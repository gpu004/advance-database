# Advanced Database

Docker-based course material for AQuery, KDB-X, and ReproZip.

## Repository contents

- [`course-materials/`](course-materials/README.md) contains the student lecture notes and worked ReproZip tutorial.
- [`aquery/`](aquery/docker-x86-linux/README.md) contains the pinned AQuery and KDB-X image.
- [`reprozip/`](reprozip/README.md) contains the pinned ReproZip image and Linux verification.
- [`example/simple_sales/`](example/simple_sales/README.md) contains a small AQuery example with three rows and one filter.

## Platform support

| Workflow | x86-64 Linux | Apple Silicon Mac | Windows |
| --- | --- | --- | --- |
| AQuery and KDB-X Docker image | Tested | Tested with Docker Desktop using `linux/amd64` | Not tested |
| ReproZip tracing Docker image | Tested | Does not work under AMD64 emulation | Not tested |

ReproZip students should use an x86-64 Linux host. Its tracer depends on Linux `ptrace` behavior that Docker Desktop's AMD64 emulation did not reproduce correctly on the tested M1 Mac.

## Getting started

Start with the [course-material index](course-materials/README.md).

## Linux verification with Modal

```bash
modal run example/simple_sales/run_on_modal.py
modal run reprozip/run_on_modal.py
```

The first command compiles an AQuery program and executes the generated q with KDB-X. The second traces, packs, inspects, unpacks, and reruns a Python program with ReproZip.
