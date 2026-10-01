# ReproZip inside QEMU on Modal

[This Modal run](https://modal.com/apps/tushardzig/main/ap-U7zZUF8b7CgRaTIjaEpPSW) passed on October 1, 2026.
The test traced the workload, packed it, unpacked it with the directory backend,
and replayed it. The test deleted the original workload and data before replay.
Replay exited with status 0, and `cmp` confirmed identical output. The bundle was reported as 5.33 MB.

The tested Modal container had no `/dev/kvm`. QEMU booted the VM with TCG, but
boot and package setup took several minutes. For repeated use, prepare and
cache a guest disk with the packages already installed. Install the packages
directly inside the VM for this workload. The test did not use Docker inside QEMU.

`artifacts.tar.gz` contains the saved `experiment.log`, `serial.log`, and
`experiment.rpz` files. The bundle's SHA-256 is
`23e7aaa1a5a2866283a9be4e9442282c4b99150b20689710af09d42e20b8bc46`.

Run from the repository root:

```sh
modal run reprozip/qemu-modal/run.py
```

The local Modal client submits the job and saves the returned `artifacts.tar.gz`.
QEMU, the Ubuntu guest, package installation, tracing, packing, and replay all
run on Modal. No QEMU or Docker process runs on the client machine.

The VM uses Ubuntu 22.04 x86-64, QEMU system emulation with TCG, 2 guest CPUs,
and 2 GiB guest RAM. The Modal function requests 4 CPUs and 4 GiB RAM and has
a 40-minute timeout. It boots a disposable disk overlay and terminates QEMU
when the experiment ends. Guest SSH only listens through a loopback forward
inside the Modal container. The Modal function generates the temporary SSH key
and excludes it from the returned artifacts.

ReproZip and ReproUnzip 1.3.2 install directly inside the VM. Docker inside the
VM would add a daemon and container permissions without helping this test.
Use that extra layer only when testing a Docker-specific workflow.

The workload reads a file, transforms its contents, launches a child process,
and writes a file. The test traces it, packs an `.rpz`, unpacks into a fresh
directory, deletes the original script and data, and replays. The test compares
the output files byte for byte. It returns the bundle, guest command log, and
boot log only if the files match.
This tests directory replay within one VM, not replay on a second machine or
the Docker unpacker.

The base cloud-image URL follows Ubuntu's current Jammy image. Modal caches the
built host image, but a new build may fetch a newer guest image. For long-term
repeatability, pin a dated cloud image and verify its published checksum.
