"""Run an x86 Linux ReproZip VM on Modal."""
from pathlib import Path
import modal

app = modal.App("reprozip-qemu-test")
image = (modal.Image.debian_slim(python_version="3.11")
         .apt_install("qemu-system-x86", "qemu-utils", "cloud-image-utils", "openssh-client", "curl")
         .run_commands("curl -fL --retry 3 https://cloud-images.ubuntu.com/jammy/current/jammy-server-cloudimg-amd64.img -o /root/base.img"))

GUEST_SCRIPT = r'''#!/bin/bash
set -euxo pipefail
export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y python3-pip python3-dev build-essential libsqlite3-dev
python3 -m pip install 'reprozip==1.3.2' 'reprounzip==1.3.2'
mkdir -p /root/experiment
cd /root/experiment
printf 'reprozip on modal qemu\n' > input.txt
cat > workload.py <<'PY'
from pathlib import Path
import subprocess
text = Path('input.txt').read_text().upper()
text += subprocess.check_output(['/bin/echo', 'CHILD PROCESS OK'], text=True)
Path('output.txt').write_text(text)
print(text, end='')
PY
uname -a
reprozip --version
reprounzip --version
reprozip trace --overwrite /usr/bin/python3 workload.py
cp output.txt expected.txt
reprozip pack experiment.rpz
reprounzip info experiment.rpz
reprounzip directory setup experiment.rpz /root/replay
# Remove the original workload and data to test use of the unpacked files.
rm workload.py input.txt output.txt
reprounzip directory run /root/replay
cmp expected.txt /root/replay/root/root/experiment/output.txt
sha256sum expected.txt /root/replay/root/root/experiment/output.txt experiment.rpz
echo REPLAY_VERIFIED
'''


@app.function(image=image, cpu=4, memory=4096, timeout=2400)
def experiment():
    import subprocess
    import time
    import tarfile

    def run(args, **kwargs):
        return subprocess.run(args, check=True, text=True, **kwargs)

    run(["ssh-keygen", "-q", "-t", "ed25519", "-N", "", "-f", "/tmp/guest-key"])
    pubkey = Path("/tmp/guest-key.pub").read_text().strip()
    Path("/tmp/user-data").write_text(
        "#cloud-config\nusers:\n  - name: root\n    ssh_authorized_keys:\n      - " + pubkey
        + "\ndisable_root: false\nssh_pwauth: false\n")
    Path("/tmp/meta-data").write_text("instance-id: reprozip-qemu\nlocal-hostname: reprozip-qemu\n")
    run(["cloud-localds", "/tmp/seed.img", "/tmp/user-data", "/tmp/meta-data"])
    run(["qemu-img", "create", "-f", "qcow2", "-F", "qcow2", "-b", "/root/base.img", "/tmp/guest.img", "10G"])
    print("Modal host KVM exists:", Path("/dev/kvm").exists(), flush=True)
    serial = open("/tmp/serial.log", "w")
    vm = subprocess.Popen([
        "qemu-system-x86_64", "-accel", "tcg,thread=multi", "-m", "2048", "-smp", "2",
        "-drive", "file=/tmp/guest.img,if=virtio", "-drive", "file=/tmp/seed.img,format=raw,if=virtio",
        "-netdev", "user,id=net0,hostfwd=tcp:127.0.0.1:2222-:22", "-device", "virtio-net-pci,netdev=net0",
        "-display", "none", "-serial", "stdio", "-monitor", "none", "-no-reboot"],
        stdout=serial, stderr=subprocess.STDOUT)
    opts = ["-i", "/tmp/guest-key", "-o", "StrictHostKeyChecking=no", "-o", "UserKnownHostsFile=/dev/null", "-o", "ConnectTimeout=5"]
    ssh = ["ssh", *opts, "-p", "2222", "root@127.0.0.1"]
    try:
        deadline = time.monotonic() + 600
        while time.monotonic() < deadline:
            if subprocess.run([*ssh, "true"], capture_output=True).returncode == 0:
                break
            if vm.poll() is not None:
                raise RuntimeError("QEMU exited: " + Path("/tmp/serial.log").read_text()[-8000:])
            time.sleep(5)
        else:
            raise RuntimeError("SSH boot timeout: " + Path("/tmp/serial.log").read_text()[-8000:])
        print("Guest SSH ready; installing and running ReproZip", flush=True)
        result = subprocess.run([*ssh, "bash -s"], input=GUEST_SCRIPT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
        Path("/tmp/experiment.log").write_text(result.stdout)
        print(result.stdout, flush=True)
        if result.returncode:
            raise RuntimeError(f"Guest experiment failed: {result.returncode}")
        run(["scp", *opts, "-P", "2222", "root@127.0.0.1:/root/experiment/experiment.rpz", "/tmp/experiment.rpz"])
        with tarfile.open("/tmp/artifacts.tar.gz", "w:gz") as archive:
            for name in ("experiment.rpz", "experiment.log", "serial.log"):
                archive.add("/tmp/" + name, arcname=name)
        return Path("/tmp/artifacts.tar.gz").read_bytes()
    finally:
        vm.terminate()
        try:
            vm.wait(timeout=10)
        except subprocess.TimeoutExpired:
            vm.kill()
            vm.wait()
        serial.close()


@app.local_entrypoint()
def main():
    # The local process only submits cloud work and saves returned artifacts.
    artifacts = experiment.remote()
    destination = Path(__file__).with_name("artifacts.tar.gz")
    destination.write_bytes(artifacts)
    print(f"Saved {destination}")
