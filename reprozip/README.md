# ReproZip on x86-64 Linux

ReproZip's tracer requires Linux system-call tracing and does not support ARM64 tracing. The course workflow therefore requires an x86-64 Linux Docker host.

Do not use Docker Desktop's AMD64 emulation on Apple Silicon for this course. The image built successfully on an M1 Mac, but `reprozip trace` reported invalid emulated syscalls and crashed even with `SYS_PTRACE`.

See the [Docker setup instructions](docker-x86-linux/README.md). Student-facing instructions are in the [ReproZip lecture notes](../course-materials/REPROZIP_LECTURE_NOTES.md) and [worked tutorial](../course-materials/REPROZIP_TUTORIAL.md).

## Verify the Linux control with Modal

```bash
modal run reprozip/run_on_modal.py
```

The smoke test traces a Python program, creates an `.rpz` bundle, inspects and unpacks it, reruns the program, and checks the reproduced output on x86-64 Debian 12.
