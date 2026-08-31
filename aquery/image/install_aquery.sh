#!/usr/bin/env bash
# Install the open-source AQuery compiler (a2q) from josepablocam/aquery.
# Linux x86_64 + Java 8 (Scala 2.11 toolchain) for Docker image builds.
#
# Pins: bump COURSIER_* / AQUERY_GIT_SHA together when upgrading.
set -euo pipefail

if [[ "$(uname -s)/$(uname -m)" != "Linux/x86_64" ]]; then
  echo "unsupported platform: $(uname -s)/$(uname -m) (need Linux/x86_64)" >&2
  exit 1
fi

export PATH="${HOME}/.local/bin:${PATH}"
AQUERY_HOME="${AQUERY_HOME:-${HOME}/.local/share/aquery}"
AQUERY_GIT_SHA="${AQUERY_GIT_SHA:-5b26f1e6f6d3ff1587c89d63a19d8fd18b49173d}"
AQUERY_REPO_URL="${AQUERY_REPO_URL:-https://github.com/josepablocam/aquery.git}"

CS="${HOME}/.local/bin/cs"
COURSIER_VERSION="${COURSIER_VERSION:-v2.1.24}"
CS_ASSET="cs-x86_64-pc-linux.gz"
# sha256 of github.com/coursier/coursier release asset cs-x86_64-pc-linux.gz @ v2.1.24
COURSIER_SHA256="${COURSIER_SHA256:-d2c0572a17fb6146ea65349b59dd216b38beff60ae22bce6e549867c6ed2eda6}"
CS_URL="https://github.com/coursier/coursier/releases/download/${COURSIER_VERSION}/${CS_ASSET}"

if command -v a2q >/dev/null 2>&1; then
  echo "AQuery compiler already available: $(command -v a2q)"
  exit 0
fi

mkdir -p "${HOME}/.local/bin" "${HOME}/.local/share"

if [[ ! -x "$CS" ]]; then
  curl -fsSL -o "${CS}.gz" "$CS_URL"
  actual_sha="$(sha256sum "${CS}.gz" | awk '{print $1}')"
  if [[ "$actual_sha" != "$COURSIER_SHA256" ]]; then
    echo "coursier ${CS_ASSET} sha256 mismatch:" >&2
    echo "  expected: ${COURSIER_SHA256}" >&2
    echo "  actual:   ${actual_sha}" >&2
    exit 1
  fi
  gzip -df "${CS}.gz"
  chmod +x "$CS"
fi

rm -rf "$AQUERY_HOME"
mkdir -p "$AQUERY_HOME"
git -C "$AQUERY_HOME" init -q
git -C "$AQUERY_HOME" remote add origin "$AQUERY_REPO_URL"
git -C "$AQUERY_HOME" fetch --depth 1 origin "$AQUERY_GIT_SHA"
git -C "$AQUERY_HOME" checkout -q FETCH_HEAD
# Record the pin for later inspection.
git -C "$AQUERY_HOME" rev-parse HEAD >"$AQUERY_HOME/.pinned_sha"
actual_sha="$(tr -d '[:space:]' <"$AQUERY_HOME/.pinned_sha")"
if [[ "$actual_sha" != "$AQUERY_GIT_SHA" ]]; then
  echo "aquery git sha mismatch: expected ${AQUERY_GIT_SHA}, got ${actual_sha}" >&2
  exit 1
fi

CP="$($CS fetch -p \
  org.scala-lang:scala-compiler:2.11.8 \
  org.scala-lang.modules:scala-parser-combinators_2.11:1.0.4 \
  org.scalaz:scalaz-core_2.11:7.2.4)"
printf '%s' "$CP" >"$AQUERY_HOME/classpath.txt"
rm -rf "$AQUERY_HOME/classes"
mkdir -p "$AQUERY_HOME/classes"

mapfile -d '' SOURCES < <(find "$AQUERY_HOME/src/main/scala" -name '*.scala' -print0)
java -Xmx2g -cp "$CP" scala.tools.nsc.Main \
  -cp "$CP" \
  -d "$AQUERY_HOME/classes" \
  "${SOURCES[@]}"

cat >"${HOME}/.local/bin/a2q" <<EOF
#!/usr/bin/env bash
CP="\$(cat '$AQUERY_HOME/classpath.txt')"
exec java -cp "$AQUERY_HOME/classes:$AQUERY_HOME/src/main/resources:\${CP}" edu.nyu.aquery.Aquery "\$@"
EOF
chmod +x "${HOME}/.local/bin/a2q"

test -x "${HOME}/.local/bin/a2q"
# a2q -h prints usage then exits 1 (by design in Aquery.scala).
help_out="$(a2q -h 2>&1 || true)"
printf '%s\n' "$help_out" | grep -q 'AQuery Compiler'

echo "Installed AQuery compiler: ${HOME}/.local/bin/a2q (sha ${AQUERY_GIT_SHA})"
