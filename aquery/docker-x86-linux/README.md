# AQuery and KDB-X with Docker

This image contains the pinned x86-64 Linux builds of AQuery, KDB-X, q, and PyKX.

It has been tested on x86-64 Linux and on Apple Silicon macOS through Docker Desktop with `--platform=linux/amd64`. Windows has not been tested for this course.

For the complete student workflow, see the [AQuery and KDB-X lecture notes](../../course-materials/AQUERY_KDBX_LECTURE_NOTES.md).

## KDB-X Community license

A KDB-X license is required.

1. Follow the [official KDB-X installation page](https://code.kx.com/kdb-x/get_started/kdb-x-install.html) to create a KX Developer account and obtain the base64-encoded Community license.
2. From the repository root, create the local environment file:

   ```bash
   cp .env.example .env
   chmod 600 .env
   ```
3. Put the complete license value in `.env`:

   ```env
   KDB_LICENSE_B64=paste_the_complete_base64_license_value_here
   ```

Do not commit `.env` or share the license.

## Build the image

Run from the repository root:

```bash
docker build --platform=linux/amd64 -t aquery:linux-x86 \
  -f aquery/docker-x86-linux/Dockerfile aquery
```

## Start q

```bash
docker run --rm -it --platform=linux/amd64 \
  --env-file .env aquery:linux-x86
```

At the q prompt, run `1+1`. Enter a single backslash to exit.

Compile and execute the simple sales example:

```bash
rm -f example/simple_sales/simple_sales.generated.q
docker run --rm --env-file .env \
  --platform=linux/amd64 \
  -v "$PWD/example/simple_sales:/work" aquery:linux-x86 \
  a2q -c -a 1 -o simple_sales.generated.q simple_sales.a
docker run --rm --env-file .env \
  --platform=linux/amd64 \
  -v "$PWD/example/simple_sales:/work" aquery:linux-x86 \
  q simple_sales.generated.q
```

The result contains `banana` with amount 7 and `coffee` with amount 12.

## Apple Silicon note

Docker Desktop runs this AMD64 image through emulation. The complete build, compile, and q execution path passed on an M1 Mac. It is slower than native ARM64 execution, especially during the first image build.
