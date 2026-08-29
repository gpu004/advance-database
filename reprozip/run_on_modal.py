"""Run a complete ReproZip smoke test on Modal's x86-64 Linux runtime.

Run from the repository root:
    modal run reprozip/run_on_modal.py
"""

from pathlib import Path
import shutil
import subprocess

import modal


ROOT = Path(__file__).resolve().parents[1] if modal.is_local() else Path("/")
DOCKERFILE = ROOT / "reprozip" / "docker-x86-linux" / "Dockerfile"

app = modal.App("reprozip-linux-smoke-test")
image = modal.Image.from_dockerfile(
    DOCKERFILE,
    context_dir=DOCKERFILE.parent,
)


def run(command: list[str], cwd: Path) -> str:
    rendered = f"$ {' '.join(command)}"
    print(rendered, flush=True)
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            text=True,
            capture_output=True,
            check=True,
            timeout=90,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"command timed out after 90 seconds: {rendered}") from exc
    output = f"{result.stdout}{result.stderr}".rstrip()
    if output:
        print(output, flush=True)
    return f"{rendered}\n{output}".rstrip()


@app.function(image=image, timeout=10 * 60)
def verify() -> str:
    work = Path("/tmp/reprozip-smoke-test")
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()

    (work / "demo.py").write_text(
        """from pathlib import Path
import sys

source = Path(sys.argv[1]).read_text()
Path(sys.argv[2]).write_text(source.upper())
"""
    )
    (work / "input.txt").write_text("reprozip on nyu linux\n")

    logs = [
        run(["uname", "-m"], work),
        run(["python3", "--version"], work),
        run(["reprozip", "--version"], work),
        run(["reprounzip", "--version"], work),
        run(
            [
                "reprozip",
                "trace",
                "python3",
                "demo.py",
                "input.txt",
                "output.txt",
            ],
            work,
        ),
    ]

    expected = "REPROZIP ON NYU LINUX\n"
    traced_output = (work / "output.txt").read_text()
    if traced_output != expected:
        raise RuntimeError(f"unexpected traced output: {traced_output!r}")

    logs.extend(
        [
            run(["reprozip", "pack", "smoke-test.rpz"], work),
            run(["reprounzip", "info", "smoke-test.rpz"], work),
            run(
                [
                    "reprounzip",
                    "directory",
                    "setup",
                    "smoke-test.rpz",
                    "unpacked",
                ],
                work,
            ),
        ]
    )

    (work / "output.txt").unlink()
    logs.append(run(["reprounzip", "directory", "run", "unpacked"], work))

    reproduced_output = (
        work / "unpacked" / "root" / "tmp" / work.name / "output.txt"
    ).read_text()
    if reproduced_output != expected:
        raise RuntimeError(f"unexpected reproduced output: {reproduced_output!r}")

    bundle_size = (work / "smoke-test.rpz").stat().st_size
    return (
        "\n\n".join(logs)
        + f"\n\ntrace output: {traced_output.strip()}"
        + f"\nreproduced output: {reproduced_output.strip()}"
        + f"\nbundle: smoke-test.rpz ({bundle_size} bytes)"
    )


@app.local_entrypoint()
def main() -> None:
    print(verify.remote())
