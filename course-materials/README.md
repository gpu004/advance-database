# AQuery, KDB-X, and ReproZip course material

Prepared for Advanced Database Systems, Fall 2026.

These notes replace the older AQuery and ReproZip material. Every installation and execution path documented here uses Docker.

## Files to share

- [`AQUERY_KDBX_LECTURE_NOTES.md`](AQUERY_KDBX_LECTURE_NOTES.md) explains AQuery, KDB-X, q, licensing, Docker setup, and the complete compile-and-run workflow.
- [`REPROZIP_LECTURE_NOTES.md`](REPROZIP_LECTURE_NOTES.md) explains the ReproZip workflow and the commands students need for a project submission.
- [`REPROZIP_TUTORIAL.md`](REPROZIP_TUTORIAL.md) is a complete worked example that traces, packs, inspects, unpacks, and reruns a small Python program.

## Platform support

| Workflow | x86-64 Linux | Apple Silicon Mac | Windows |
| --- | --- | --- | --- |
| AQuery and KDB-X in Docker | Course test passed | Course test passed with Docker Desktop using `linux/amd64` | Not tested |
| ReproZip tracing in Docker | Course test passed | Course test failed | Not tested |

The AQuery image ran successfully on an M1 Mac through Docker Desktop's AMD64 emulation. Native KDB-X and AQuery also worked on that Mac, but the course instructions use Docker so every student follows the same workflow.

ReproZip requires Linux `ptrace`. On the tested M1 Mac, its AMD64 Docker container reported invalid emulated syscalls and crashed during tracing even with `SYS_PTRACE`. Students must use an x86-64 Linux host for ReproZip.

Students using CIMS should connect through `access.cims.nyu.edu`, then move to the compute server assigned for the course. They should not compile or run coursework on the access gateway. Course staff must confirm that the assigned compute server provides Docker and permits `ptrace`.

## Installation links for the course website

- Docker Desktop: <https://docs.docker.com/desktop/>
- KDB-X and q: <https://code.kx.com/kdb-x/get_started/kdb-x-install.html>
- Course repository: <https://github.com/gpu004/advance-database>
- ReproZip: <https://github.com/VIDA-NYU/reprozip#quickstart>
- ReproUnzip: <https://reprozip.readthedocs.io/en/latest/unpacking.html>
- NYU CIMS access servers: <https://cims.nyu.edu/dynamic/systems/resources/accessservers/>

## Validation record

The Linux controls passed on x86-64 Debian 12 through Modal on August 30, 2026.

- AQuery generated an 8,002-byte q program from the three-row sales example.
- KDB-X ran the generated program and returned `banana = 7` and `coffee = 12` for the `amount > 5` filter.
- ReproZip 1.3.2 traced and packed a Python command.
- ReproUnzip 1.3.2 inspected, unpacked, and reran the command.
- The traced and reproduced outputs both contained `REPROZIP ON NYU LINUX`.

The AQuery Docker workflow also passed on an Apple M1 Mac with Docker Desktop 4.87. The ReproZip trace failed on that Mac and is intentionally excluded from the Mac instructions.

The remaining host-specific check is whether the assigned NYU compute server provides Docker and permits ReproZip to use `ptrace`.
