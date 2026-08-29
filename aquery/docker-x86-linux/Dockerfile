FROM --platform=linux/amd64 azul/zulu-openjdk@sha256:772cff8aa0094d620beb36d2e068db8e6b7e18da9ce7edf8a44826a8adbfd6b6

ENV DEBIAN_FRONTEND=noninteractive \
    KDBX_HOME=/opt/kx \
    QHOME=/opt/kx \
    QLIC=/tmp/kx-lic \
    PATH=/opt/kx/bin:/root/.local/bin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl file git gzip unzip rlwrap python3 python3-venv \
    && rm -rf /var/lib/apt/lists/* \
    && ln -sf /usr/bin/python3 /usr/local/bin/python

COPY --from=ghcr.io/astral-sh/uv@sha256:eb2843a1e56fd9e30c7276ce1a52cba86e64c7b385f5e3279a0e08e02dd058fc /uv /usr/local/bin/uv
COPY --chmod=755 image/install_kdbx.sh image/install_aquery.sh /opt/
COPY --chmod=755 image/with_kx_license.sh /opt/kx/with-kx-license

RUN /opt/install_kdbx.sh \
    && /opt/install_aquery.sh \
    && uv pip install --system "pykx==4.0.0"

WORKDIR /work
ENTRYPOINT ["/opt/kx/with-kx-license"]
CMD ["q"]
