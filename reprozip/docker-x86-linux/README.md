# ReproZip with Docker on x86 Linux

This image contains ReproZip 1.3.2 and ReproUnzip 1.3.2. It requires an x86 Linux Docker host.

Student instructions: start with the [ReproZip lecture notes](../../course-materials/REPROZIP_LECTURE_NOTES.md). This file is the build/run reference for the image.

ReproZip tracing needs x86 Linux. Mac M-series Docker fails. See [platform support](../../course-materials/README.md#platform-support).

## Build the image

Run from the repository root:

```bash
docker build --platform=linux/amd64 -t reprozip:linux-x86 \
  -f reprozip/docker-x86-linux/Dockerfile reprozip/docker-x86-linux
```

## Start the container

ReproZip uses `ptrace`. `--cap-add=SYS_PTRACE` is recommended because older Docker or kernel versions require it:

```bash
docker run --rm -it --platform=linux/amd64 \
  --cap-add=SYS_PTRACE \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD:/work" -w /work \
  reprozip:linux-x86
```

`--user` runs the container as your host user, so files it creates belong to you and you can edit or delete them without `sudo`. `-e HOME=/tmp` gives ReproZip a writable home directory. The shell prompt may show `I have no name!`; this is expected.

Files created below `/work` remain in the host directory after the container exits.

Inside the container, trace and pack a working command:

```bash
reprozip trace python3 demo.py input.txt output.txt
reprozip pack project.rpz
reprounzip info project.rpz
```

See the [worked tutorial](../../course-materials/REPROZIP_TUTORIAL.md) for the trace, pack, inspect, unpack, and rerun sequence.
