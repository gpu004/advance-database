# ReproZip with Docker on x86-64 Linux

This image contains ReproZip 1.3.2 and ReproUnzip 1.3.2. It requires an x86-64 Linux Docker host.

Apple Silicon Docker Desktop is not supported for this workflow. AMD64 emulation failed during `reprozip trace` on the tested M1 Mac.

## Build the image

Run from the repository root:

```bash
docker build --platform=linux/amd64 -t reprozip:linux-x86 \
  -f reprozip/docker-x86-linux/Dockerfile reprozip/docker-x86-linux
```

## Start the container

ReproZip uses `ptrace`, so the container needs `SYS_PTRACE`:

```bash
docker run --rm -it --platform=linux/amd64 \
  --cap-add=SYS_PTRACE \
  -v "$PWD:/work" -w /work \
  reprozip:linux-x86
```

Files created below `/work` remain in the host directory after the container exits.

Inside the container, trace and pack a working command:

```bash
reprozip trace python3 demo.py input.txt output.txt
reprozip pack project.rpz
reprounzip info project.rpz
```

See the [worked tutorial](../../course-materials/REPROZIP_TUTORIAL.md) for the complete trace, pack, inspect, unpack, and rerun sequence.
