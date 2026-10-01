#!/usr/bin/env bash
# Decode KDB_LICENSE_B64 into kc.lic, then run the requested command.
# Pass the license to Docker with --env-file .env from the repository root.
set -euo pipefail
[[ -n "${KDB_LICENSE_B64:-}" ]] || {
  echo "KDB_LICENSE_B64 unset (use docker --env-file .env)" >&2
  exit 1
}
lic_dir="${QLIC:-/tmp/kx-lic}"
mkdir -p "$lic_dir"
printf '%s' "$KDB_LICENSE_B64" | base64 --decode >"$lic_dir/kc.lic"
chmod 0600 "$lic_dir/kc.lic"
export QLIC="$lic_dir" QHOME="${QHOME:-${KDBX_HOME:-/opt/kx}}"
exec "$@"
