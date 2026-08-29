# ReproZip on x86-64 Linux

ReproZip's tracer requires x86-64 Linux and does not support arm64 tracing ([issue #385](https://github.com/VIDA-NYU/reprozip/issues/385)). See the [Docker setup instructions](docker-x86-linux/README.md).

## Verify on Modal

```bash
modal run reprozip/run_on_modal.py
```

The smoke test traces a Python program, creates an `.rpz` bundle, inspects and
unpacks it, reruns the program, and checks the reproduced output.
