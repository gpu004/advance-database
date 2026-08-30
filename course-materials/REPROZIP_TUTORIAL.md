# ReproZip worked tutorial

This tutorial creates a small Python program, traces it, builds an `.rpz` bundle, and reruns it through ReproUnzip.

## 1. Install the tools

Use x86-64 Linux:

```bash
uname -m
```

The output must be `x86_64`.

Create and activate a virtual environment:

```bash
python3 -m venv "$HOME/.venvs/reprozip"
source "$HOME/.venvs/reprozip/bin/activate"
python -m pip install --upgrade pip
python -m pip install reprozip==1.3.2 reprounzip==1.3.2
```

Check the installed versions:

```bash
reprozip --version
reprounzip --version
```

## 2. Create the example

```bash
mkdir -p "$HOME/reprozip-demo"
cd "$HOME/reprozip-demo"
```

Save this program as `demo.py`:

```python
from pathlib import Path
import sys

text = Path(sys.argv[1]).read_text()
Path(sys.argv[2]).write_text(text.upper())
```

Create an input file:

```bash
printf 'reprozip on nyu linux\n' > input.txt
```

The directory should now contain:

```text
demo.py
input.txt
```

## 3. Run the program normally

```bash
python3 demo.py input.txt output.txt
cat output.txt
```

Expected output:

```text
REPROZIP ON NYU LINUX
```

Stop and fix the program if this command fails.

## 4. Trace the command

Run the same command through ReproZip:

```bash
reprozip trace python3 demo.py input.txt output.txt
```

Confirm that the trace exists:

```bash
ls -la .reprozip-trace
less .reprozip-trace/config.yml
```

Check the recorded command and review the file list for credentials, private files, and unrelated data.

## 5. Create the bundle

```bash
reprozip pack smoke-test.rpz
ls -lh smoke-test.rpz
```

This creates the file to transfer or submit:

```text
smoke-test.rpz
```

## 6. Inspect the bundle

```bash
reprounzip info smoke-test.rpz
reprounzip showfiles smoke-test.rpz
```

The information should include:

- architecture `x86_64`
- the command `python3 demo.py input.txt output.txt`
- compatible unpackers including `directory`
- named input and output files

## 7. Reproduce it in a fresh directory

Create a separate test directory:

```bash
mkdir -p "$HOME/reprozip-check"
cd "$HOME/reprozip-check"
```

Set up the bundle:

```bash
reprounzip directory setup "$HOME/reprozip-demo/smoke-test.rpz" unpacked
```

Run the recorded command:

```bash
reprounzip directory run unpacked
```

The command must finish with status 0.

Find the reproduced output:

```bash
find unpacked -name output.txt -print
```

Inspect the path printed by `find`:

```bash
cat /path/printed/by/find/output.txt
```

Expected output:

```text
REPROZIP ON NYU LINUX
```

The original output and reproduced output must match.

## 8. Replace an input

First inspect the file identifiers:

```bash
reprounzip showfiles "$HOME/reprozip-demo/smoke-test.rpz"
```

The example normally labels the command-line input as `arg2` and the output as `arg3`. Always use the identifiers printed by your own bundle.

Create a replacement input:

```bash
printf 'second test\n' > new_input.txt
```

Upload and run it:

```bash
reprounzip directory upload unpacked new_input.txt:arg2
reprounzip directory run unpacked
```

Download the new output:

```bash
reprounzip directory download unpacked arg3:result.txt
cat result.txt
```

Expected output:

```text
SECOND TEST
```

## 9. What to submit for a course project

At minimum, submit:

- one clearly named `.rpz` bundle
- a README with the recorded command
- the expected output
- the language and runtime version
- any assumptions about the input files or host

Before submitting, repeat `reprounzip directory setup` and `reprounzip directory run` in a fresh directory. Do not assume that a successful `reprozip pack` command proves the bundle can be reproduced.

## Verified reference result

This workflow was tested on x86-64 Debian 12 with Python 3.11.14, ReproZip 1.3.2, and ReproUnzip 1.3.2. The trace and reproduced run both produced `REPROZIP ON NYU LINUX`.

The assigned NYU compute server must still permit `ptrace`, which ReproZip uses to record system calls.
