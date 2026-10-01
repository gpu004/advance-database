# Reproduce a small Python sales calculation

This example adds the revenue in `sales.csv` and prints:

```text
Total revenue: 45
```

The script uses only Python's standard library. Use x86 Linux with Docker. Do not use Mac M-series Docker for ReproZip tracing.

## Start the course container

Run from the repository root:

```bash
docker build --platform=linux/amd64 -t reprozip:linux-x86 \
  -f reprozip/docker-x86-linux/Dockerfile reprozip/docker-x86-linux

docker run --rm -it --platform=linux/amd64 \
  --cap-add=SYS_PTRACE \
  -v "$PWD/example/reprozip_sales:/work" -w /work \
  reprozip:linux-x86
```

Run the remaining commands inside the container.

## Run the program normally

The directory already contains [`sales.csv`](sales.csv) and [`total.py`](total.py).

```bash
python3 total.py
```

Expected output:

```text
Total revenue: 45
```

## Trace the working command

```bash
reprozip trace python3 total.py
```

Tracing executes the script. ReproZip records `total.py`, `sales.csv`, the Python executable, and supporting files used during the run.

## Review the configuration

Open `.reprozip-trace/config.yml` with your text editor on the host. Check the recorded command and file list for credentials, private files, or unrelated data before packing.

## Create the bundle

```bash
reprozip pack sales-demo.rpz
```

Keep `total.py` and `sales.csv` unchanged between tracing and packing. Packing copies their contents at that point.

See the [ReproZip packing documentation](https://reprozip.readthedocs.io/en/latest/packing.html).

## Inspect and reproduce the bundle

These commands also work on another compatible Linux machine with ReproUnzip installed, after copying `sales-demo.rpz` there:

```bash
reprounzip info sales-demo.rpz
reprounzip showfiles sales-demo.rpz

reprounzip directory setup sales-demo.rpz replay
reprounzip directory run replay
```

`setup` extracts the experiment into `replay/`. `run` executes the recorded command.

Expected output:

```text
Total revenue: 45
```

The directory backend does not isolate the program from the host filesystem. Reproduce only trusted bundles. ReproUnzip also offers Docker and virtual-machine backends through plugins. See the [unpacking documentation](https://reprozip.readthedocs.io/en/latest/unpacking.html).

Enter `exit` to leave the container. The bundle, trace, and replay directory remain in `example/reprozip_sales/` on the host.

For another run, remove only the generated `.reprozip-trace/`, `sales-demo.rpz`, and `replay/` entries. Keep the two source files.

## Verification

Tested on Modal in an x86 Linux guest. The original and reproduced outputs both printed `Total revenue: 45`. Replay also passed after moving the original Python and CSV files away from their recorded paths.
