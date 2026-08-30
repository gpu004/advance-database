# ReproZip on x86-64 Linux

## What ReproZip does

ReproZip records one command and the files that command uses. It can then create an `.rpz` bundle containing the program, data, libraries, environment information, and recorded command. ReproUnzip inspects the bundle and reruns the command.

```text
working command  ->  reprozip trace  ->  reprozip pack  ->  reprounzip run
```

ReproZip does not repair a failing program. Run the original command successfully before tracing it.

## Platform

ReproZip tracing requires Linux. These course instructions target x86-64 Linux.

Students using CIMS should connect through the access server and then move to the assigned compute server:

```bash
ssh <netid>@access.cims.nyu.edu
ssh <course-compute-server>
hostname
uname -m
python3 --version
```

Do not run coursework on `access.cims.nyu.edu`. The instructor should supply the compute-server hostname.

## Install without sudo

Create a Python virtual environment in the home directory:

```bash
python3 -m venv "$HOME/.venvs/reprozip"
source "$HOME/.venvs/reprozip/bin/activate"
python -m pip install --upgrade pip
python -m pip install reprozip==1.3.2 reprounzip==1.3.2
```

Verify the installation:

```bash
which python
which reprozip
reprozip --version
reprounzip --version
```

Activate the environment again after a new login:

```bash
source "$HOME/.venvs/reprozip/bin/activate"
```

If `python3 -m venv` fails, do not use sudo. Record the hostname and complete error, then ask course staff which Python environment students should use.

## The required workflow

### 1. Test the original command

Run the command normally and inspect its output:

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
less .reprozip-trace/config.yml
```

Before packing, inspect `config.yml` for:

- private keys, passwords, access tokens, and credentials
- licensed files that must not be distributed
- browser profiles or unrelated files from the home directory
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

`reprounzip showfiles` reports the named input and output files that can be replaced or downloaded.

### 5. Test the bundle in a fresh directory

Do not test only inside the original project folder.

```bash
mkdir -p "$HOME/reprozip-check"
cd "$HOME/reprozip-check"
reprounzip directory setup /path/to/project.rpz unpacked
reprounzip directory run unpacked
```

A successful run exits with status 0 and produces the expected output below the `unpacked` directory.

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

```bash
java -jar project.jar input.txt output.txt
reprozip trace java -jar project.jar input.txt output.txt
```

### C or C++

```bash
g++ -O2 -o project project.cpp
./project input.txt output.txt
reprozip trace ./project input.txt output.txt
```

### Shell script

```bash
chmod +x run.sh
./run.sh
reprozip trace ./run.sh
```

## Final-project bundle checklist

- The program runs normally on the assigned x86-64 Linux compute server.
- The traced command covers every required test or input.
- `.reprozip-trace/config.yml` contains no credentials or unrelated personal files.
- The `.rpz` filename identifies the project or team.
- `reprounzip info` reports the intended command and architecture.
- `reprounzip directory setup` succeeds in a fresh directory.
- `reprounzip directory run` exits with status 0.
- The reproduced output matches the expected output.
- The submission README states the command, expected result, language version, and assumptions.

## Troubleshooting

### `reprozip: command not found`

```bash
source "$HOME/.venvs/reprozip/bin/activate"
which reprozip
```

### Wrong architecture

```bash
uname -m
```

Use the assigned x86-64 compute server.

### Trace fails or hangs

ReproZip uses Linux `ptrace`. Record the hostname, kernel, exact command, ReproZip version, and complete error. Ask course staff whether `ptrace` is allowed on that host.

### Bundle is unexpectedly large

Inspect `.reprozip-trace/config.yml`, remove unrelated files from the configuration, and trace again if needed.

### Reproduced run misses a file

Test in a fresh directory. Retrace while the original program opens every required file.

## References

- ReproZip quickstart: <https://github.com/VIDA-NYU/reprozip#quickstart>
- ReproZip packing: <https://reprozip.readthedocs.io/en/latest/packing.html>
- ReproUnzip: <https://reprozip.readthedocs.io/en/latest/unpacking.html>
- Course setup and smoke test: <https://github.com/gpu004/advance-database>
- NYU CIMS access servers: <https://cims.nyu.edu/dynamic/systems/resources/accessservers/>
