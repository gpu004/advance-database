# ReproZip with Docker on x86 Linux

The course ReproZip tracing workflow requires x86 Linux. Tracing failed with Mac M-series Docker during course testing. See [platform support](README.md#platform-support) for the tested hosts.

## What ReproZip does

ReproZip records one command and the files that command uses. It creates an `.rpz` bundle containing the program, data, libraries, environment information, and recorded command. ReproUnzip inspects the bundle and reruns the command.

```text
working command  ->  reprozip trace  ->  reprozip pack  ->  reprounzip run
```

ReproZip does not repair a failing program. Run the original command successfully before tracing it.

Every command in these notes runs inside the course Docker image. Students do not install ReproZip, ReproUnzip, or Python packages directly on the host.

ReproZip traces Linux system calls with `ptrace`. The course workflow requires an x86 Linux Docker host.

Students without an x86 Linux desktop should use the compute server assigned for the course.

## Connect to the course server

Students using CIMS should connect through the access server and then move to the assigned compute server:

```bash
ssh <netid>@access.cims.nyu.edu
ssh <course-compute-server>
hostname
uname -s
uname -m
docker version
```

The operating system must be Linux and `uname -m` must print `x86_64`. Do not run coursework on `access.cims.nyu.edu`. The instructor must provide the compute-server hostname and confirm that Docker is available there.

If Docker is unavailable or prohibited, stop and ask course staff for the approved container runtime. Do not install a system daemon on a shared server.

## Get the course repository

```bash
git clone https://github.com/gpu004/advance-database.git
cd advance-database
```

Run the remaining setup commands from the repository root.

## Build the course image

```bash
docker build --platform=linux/amd64 -t reprozip:linux-x86 \
  -f reprozip/docker-x86-linux/Dockerfile reprozip/docker-x86-linux
```

Confirm the image architecture:

```bash
docker image inspect reprozip:linux-x86 \
  --format 'os={{.Os}} architecture={{.Architecture}}'
```

Expected result:

```text
os=linux architecture=amd64
```

## Start the course container

Change to the project directory that contains the program and its inputs. Then start the container:

```bash
docker run --rm -it --platform=linux/amd64 \
  --cap-add=SYS_PTRACE \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD:/work" -w /work \
  reprozip:linux-x86
```

`--user` runs the container as your host user. You own the files it creates and can edit or delete them without `sudo`. `-e HOME=/tmp` gives ReproZip a writable home directory. The shell prompt may show `I have no name!` because the container has no username for your user ID.

`--cap-add=SYS_PTRACE` is recommended for tracing. Recent Docker versions allow `ptrace` by default, but older Docker or kernel versions and some hosts require this flag. The bind mount maps the current host directory to `/work`, so traces and bundles remain on the host after the container exits.

The remaining commands in the required workflow run inside this container.

## The required workflow

### 1. Test the original command

Run the program normally and inspect its output:

```bash
python3 demo.py input.txt output.txt
cat output.txt
```

Fix program errors before using ReproZip.

### 2. Trace the exact command

Prefix the working command with `reprozip trace`:

```bash
reprozip trace python3 demo.py input.txt output.txt
```

A successful trace creates `.reprozip-trace/config.yml`.

```bash
ls -la .reprozip-trace
cat .reprozip-trace/config.yml
```

Before packing, inspect `config.yml` for:

- private keys, passwords, access tokens, and credentials
- licensed files that must not be distributed
- browser profiles or unrelated files
- large datasets that should not be included
- the exact command the grader should run

### 3. Pack the trace

```bash
reprozip pack project.rpz
ls -lh project.rpz
```

The `.rpz` file is the portable bundle.

### 4. Inspect the bundle

```bash
reprounzip info project.rpz
reprounzip showfiles project.rpz
```

`reprounzip info` reports the architecture, Linux distribution, recorded command, software packages, and compatible unpackers.

`reprounzip showfiles` reports named input and output files that can be replaced or downloaded.

### 5. Test the bundle in a fresh directory

Do not test only beside the original program.

```bash
mkdir -p bundle-check
reprounzip directory setup project.rpz bundle-check/unpacked
reprounzip directory run bundle-check/unpacked
```

A successful run exits with status 0. Inspect the reproduced output under `bundle-check/unpacked/root/work/`.

## Multiple runs and test cases

Students may trace several runs:

```bash
reprozip trace --overwrite python3 main.py input1.txt output1.txt
reprozip trace --continue python3 main.py input2.txt output2.txt
reprozip pack project-tests.rpz
```

Another option is to trace one script that runs every required test:

```bash
chmod +x run_tests.sh
./run_tests.sh
reprozip trace ./run_tests.sh
reprozip pack project-tests.rpz
```

The traced command should exercise every file and dependency the grader needs.

## Common project commands

### Python

```bash
reprozip trace python3 main.py input.txt output.txt
```

### Java

The course image does not include Java. Extend the Dockerfile with the required pinned JDK before tracing a Java project. Do not install Java interactively in a running container because that change disappears when the container exits.

### C or C++

The course image does not include a compiler. Extend the Dockerfile with the required pinned compiler before tracing a C or C++ project.

### Shell script

```bash
chmod +x run.sh
./run.sh
reprozip trace ./run.sh
```

## Final-project bundle checklist

- The original program runs inside the course image on an x86 Linux Docker host.
- The traced command covers every required test or input.
- `.reprozip-trace/config.yml` contains no credentials or unrelated personal files.
- The `.rpz` filename identifies the project or team.
- `reprounzip info` reports the intended command and architecture.
- `reprounzip directory setup` succeeds in a fresh directory.
- `reprounzip directory run` exits with status 0.
- The reproduced output matches the expected output.
- The submission README states the command, expected result, language version, and assumptions.

## Troubleshooting

### Docker server is unavailable

If `docker version` cannot connect to the daemon, ask course staff which x86 Linux host provides the approved Docker service.

### Wrong host architecture

```bash
uname -m
```

Use an x86 Linux host. Do not use Mac M-series Docker for ReproZip tracing.

### Trace reports a permission error

Exit the container and confirm that the `docker run` command includes:

```text
--cap-add=SYS_PTRACE
```

If tracing still fails, record the hostname, kernel, Docker version, exact command, ReproZip version, and complete error. Ask course staff whether that host permits `ptrace`.

### Trace directory already exists

```text
Trace directory .reprozip-trace exists
Please use either --continue or --overwrite
```

An earlier trace is still in the project directory. Use `reprozip trace --overwrite <command>` to replace it, or `reprozip trace --continue <command>` to add another run to the same bundle. If `reprounzip directory setup` reports `Target directory exists`, remove that unpacked directory first.

### Cannot delete files created by the container

A container started without `--user` creates files owned by `root`. On the host, `rm` fails with `Permission denied` inside root-owned directories. Your program also cannot overwrite root-owned output files. From the project directory, use a root container to remove the generated files and directories. For later runs, use the `docker run` command above with `--user`.

For the workflow in these notes, the generated paths are the trace, the bundle, the unpacked directory, and the program output:

```bash
docker run --rm -v "$PWD:/work" -w /work reprozip:linux-x86 \
  rm -rf .reprozip-trace bundle-check project.rpz output.txt
```

For the [worked tutorial](REPROZIP_TUTORIAL.md), run this from `$HOME/reprozip-demo`:

```bash
docker run --rm -v "$PWD:/work" -w /work reprozip:linux-x86 \
  rm -rf .reprozip-trace check smoke-test.rpz output.txt new_input.txt result.txt
```

For the [Python sales example](../example/reprozip_sales/README.md), run this from `example/reprozip_sales`:

```bash
docker run --rm -v "$PWD:/work" -w /work reprozip:linux-x86 \
  rm -rf .reprozip-trace replay sales-demo.rpz
```

For your own project, list every file or directory the container created, including program outputs and test-run directories. Never include source or input files.

### Bundle is unexpectedly large

Inspect `.reprozip-trace/config.yml`, remove unrelated files from the configuration, and trace again if needed.

### Reproduced run misses a file

Test in a fresh directory. Retrace while the original program opens every required file.

The [validation record](README.md#validation-record) documents passing tests on August 30, 2026.

## References

- ReproZip quickstart: <https://github.com/VIDA-NYU/reprozip#quickstart>
- ReproZip packing: <https://reprozip.readthedocs.io/en/latest/packing.html>
- ReproUnzip: <https://reprozip.readthedocs.io/en/latest/unpacking.html>
- Course repository: <https://github.com/gpu004/advance-database>
- NYU CIMS access servers: <https://cims.nyu.edu/dynamic/systems/resources/accessservers/>
