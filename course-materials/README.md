# AQuery, KDB-X, and ReproZip course material

Prepared for Advanced Database Systems, Fall 2026.

These notes replace the older AQuery and ReproZip material. They target x86-64 Linux and use current KDB-X, q, AQuery, ReproZip, and ReproUnzip commands.

## Files

- [`AQUERY_KDBX_LECTURE_NOTES.md`](AQUERY_KDBX_LECTURE_NOTES.md) explains what AQuery and KDB-X do, how to install them without sudo, how to run q, and how to compile an AQuery program.
- [`REPROZIP_LECTURE_NOTES.md`](REPROZIP_LECTURE_NOTES.md) explains the ReproZip workflow and the commands students need for a project submission.
- [`REPROZIP_TUTORIAL.md`](REPROZIP_TUTORIAL.md) is a complete worked example that traces, packs, inspects, unpacks, and reruns a small Python program.

## Platform

The instructions require x86-64 Linux.

Students using CIMS should connect through `access.cims.nyu.edu`, then move to the compute server assigned for the course. They should not compile or run coursework on the access gateway.

Before installing anything, run:

```bash
hostname
uname -s
uname -m
python3 --version
```

The expected operating system is Linux and the expected architecture is `x86_64`.

## Installation links for the course website

- KDB-X and q: <https://code.kx.com/kdb-x/get_started/kdb-x-install.html>
- Course AQuery setup: <https://github.com/gpu004/advance-database>
- ReproZip: <https://github.com/VIDA-NYU/reprozip#quickstart>
- ReproUnzip: <https://reprozip.readthedocs.io/en/latest/unpacking.html>
- NYU CIMS access servers: <https://cims.nyu.edu/dynamic/systems/resources/accessservers/>

## Repository implementation

- AQuery Dockerfile: [`aquery/docker-x86-linux/Dockerfile`](../aquery/docker-x86-linux/Dockerfile)
- AQuery and KDB-X install scripts: [`aquery/image/`](../aquery/image/)
- Simple AQuery example: [`example/simple_sales/`](../example/simple_sales/)
- ReproZip Dockerfile: [`reprozip/docker-x86-linux/Dockerfile`](../reprozip/docker-x86-linux/Dockerfile)
- ReproZip Linux verification: [`reprozip/run_on_modal.py`](../reprozip/run_on_modal.py)

## Validation record

The course examples were tested on x86-64 Linux on August 29, 2026.

- AQuery compiled a three-row sales example into q.
- KDB-X ran the generated program and returned `banana = 7` and `coffee = 12` for the `amount > 5` filter.
- ReproZip 1.3.2 traced and packed a Python command.
- ReproUnzip 1.3.2 inspected, unpacked, and reran the command.
- The traced and reproduced outputs both contained `REPROZIP ON NYU LINUX`.

The remaining host-specific check is whether the assigned NYU compute server provides the required Java runtime and permits ReproZip to use `ptrace`.
