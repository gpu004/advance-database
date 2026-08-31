# AQuery and KDB-X with Docker

This image contains the pinned x86-64 Linux builds of AQuery, KDB-X, q, and PyKX.

It has been tested on x86 Linux and with Mac M-series Docker using `--platform=linux/amd64`.

Student instructions: start with the [AQuery and KDB-X lecture notes](../../course-materials/AQUERY_KDBX_LECTURE_NOTES.md). Complete the [KDB-X Community license setup](../../course-materials/AQUERY_KDBX_LECTURE_NOTES.md#get-a-kdb-x-community-license) there before using this build/run reference.

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

## Mac M-series Docker note

Docker Desktop runs this AMD64 image through emulation. The build, compile, and q execution path passed with Mac M-series Docker on an M1 Mac. It is slower than native ARM64 execution, especially during the first image build.
