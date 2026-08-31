#!/usr/bin/env bash
# Install KDB-X (q) for Linux x86_64 Docker image builds.
# Installation docs: https://code.kx.com/kdb-x/get_started/kdb-x-install.html
# Binary only. Docker provides KDB_LICENSE_B64 at runtime through .env.
#
# Pins: bump KDBX_VERSION + KDBX_L64_SHA256 together when upgrading.
set -euo pipefail

KDBX_HOME="${KDBX_HOME:-/opt/kx}"
# Resolved from portal ~latest~ redirect on 2026-07-15 → 5.0.20260706.
KDBX_VERSION="${KDBX_VERSION:-5.0.20260706}"
KDBX_L64_SHA256="${KDBX_L64_SHA256:-d4588ad228063a79a145281249dc01262a4d88146f6b5c085b0ea31acb605691}"
BASE_URL="https://portal.dl.kx.com/assets/raw/kdb-x/kdb-x/${KDBX_VERSION}"
PREFIX=l64

os="$(uname -s)"
arch="$(uname -m)"
if [[ "$os/$arch" != "Linux/x86_64" ]]; then
  echo "unsupported platform: $os/$arch (need Linux/x86_64)" >&2
  exit 1
fi

TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Downloading KDB-X ${PREFIX}.zip from ${BASE_URL}"
curl -fsSL -o "${TMP}/${PREFIX}.zip" "${BASE_URL}/${PREFIX}.zip"

actual_sha="$(sha256sum "${TMP}/${PREFIX}.zip" | awk '{print $1}')"
if [[ "$actual_sha" != "$KDBX_L64_SHA256" ]]; then
  echo "KDB-X ${PREFIX}.zip sha256 mismatch:" >&2
  echo "  expected: ${KDBX_L64_SHA256}" >&2
  echo "  actual:   ${actual_sha}" >&2
  exit 1
fi

unzip -q -o "${TMP}/${PREFIX}.zip" -d "${TMP}/extracted"

Q_BINARY="${TMP}/extracted/${PREFIX}/q"
if [[ ! -x "$Q_BINARY" ]]; then
  echo "expected ${PREFIX}/q in archive" >&2
  find "${TMP}/extracted" -type f -name q >&2 || true
  exit 1
fi

mkdir -p "${KDBX_HOME}/bin" "${KDBX_HOME}/q" "${KDBX_HOME}/mod"
install -m 0755 "$Q_BINARY" "${KDBX_HOME}/bin/q"

# ELF x86-64 check — do not invoke q (needs a license).
file "${KDBX_HOME}/bin/q" | grep -Eq 'ELF.*(x86-64|x86_64|AMD64)' || {
  echo "installed q is not an x86-64 ELF binary:" >&2
  file "${KDBX_HOME}/bin/q" >&2
  exit 1
}

cat >"${KDBX_HOME}/env.sh" <<EOF
export KDBX_HOME="${KDBX_HOME}"
export QHOME="\${QHOME:-${KDBX_HOME}}"
export PATH="${KDBX_HOME}/bin:\${PATH}"
EOF

echo "Installed KDB-X ${KDBX_VERSION} q at ${KDBX_HOME}/bin/q"
