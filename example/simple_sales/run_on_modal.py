"""Compile and execute the simple AQuery sales example on x86-64 Linux.

Run from the repository root:
    modal run example/simple_sales/run_on_modal.py
"""

from pathlib import Path
import subprocess

import modal

ROOT = Path(__file__).resolve().parents[2] if modal.is_local() else Path("/")
AQUERY = ROOT / "aquery"
EXAMPLE = ROOT / "example" / "simple_sales"

app = modal.App("aquery-simple-sales")
image = modal.Image.from_dockerfile(
    AQUERY / "docker-x86-linux" / "Dockerfile",
    context_dir=AQUERY,
)
if modal.is_local():
    image = image.add_local_dir(EXAMPLE, remote_path="/work")

kx_license = modal.Secret.from_name("kx-license", required_keys=["KDB_LICENSE_B64"])


@app.function(image=image, secrets=[kx_license], timeout=10 * 60)
def verify() -> str:
    generated = Path("/work/simple_sales.generated.q")
    generated.unlink(missing_ok=True)

    subprocess.run(
        ["a2q", "-c", "-a", "1", "-o", generated.name, "simple_sales.a"],
        cwd="/work",
        check=True,
    )
    q_result = subprocess.run(
        ["/opt/kx/with-kx-license", "q", generated.name],
        cwd="/work",
        text=True,
        capture_output=True,
        check=True,
    )
    output = q_result.stdout + q_result.stderr
    expected_fragments = ["`banana`coffee", "7 12"]
    missing = [fragment for fragment in expected_fragments if fragment not in output]
    if missing:
        raise RuntimeError(
            f"q output is missing expected fragments: {missing}\n{output}"
        )

    return (
        f"compile: ok\ngenerated: {generated.stat().st_size} bytes\nq output:\n{output}"
    )


@app.local_entrypoint()
def main() -> None:
    print(verify.remote())
