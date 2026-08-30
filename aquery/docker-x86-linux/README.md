# AQuery and KDB-X on x86-64 Linux

For the native, no-sudo installation path, see the [AQuery and KDB-X course notes](../../course-materials/AQUERY_KDBX_LECTURE_NOTES.md).

## KDB-X Community license

A kdb+ license is required.

1. [Sign up with KX](https://developer.kx.com/products/kdb-x/install) and copy your community license from the KX website.
2. From the repository root, create your local environment file:
   ```sh
   cp .env.example .env
   ```
3. Open `.env` and paste the license after `KDB_LICENSE_B64=`:
   ```env
   KDB_LICENSE_B64=paste_your_license_here
   ```

<img width="2746" height="1436" alt="KX license sign-up page" src="https://github.com/user-attachments/assets/6107d3ed-5f82-4cad-806b-47e656972786" />

<img width="2824" height="1402" alt="KX license download page" src="https://github.com/user-attachments/assets/518a167e-7f36-4e87-a470-7013c5ed84c4" />

## Docker

Requires an x86-64 Linux host.

```bash
docker build --platform=linux/amd64 -t aquery:linux-x86 \
  -f aquery/docker-x86-linux/Dockerfile aquery

docker run --rm -it --env-file .env aquery:linux-x86
```

Compile and execute the simple sales example:

```bash
rm -f example/simple_sales/simple_sales.generated.q
docker run --rm --env-file .env \
  -v "$PWD/example/simple_sales:/work" aquery:linux-x86 \
  a2q -c -a 1 -o simple_sales.generated.q simple_sales.a
docker run --rm --env-file .env \
  -v "$PWD/example/simple_sales:/work" aquery:linux-x86 \
  q simple_sales.generated.q
```

The result contains `banana` with amount 7 and `coffee` with amount 12.
