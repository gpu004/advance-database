# HW1 Q11 — AQuery maximum loss per stock

Source: `../database-interview/hw1/aquery/` (same files).

## (i) Executable AQuery

`max_loss.a` — uses built-ins `maxs`, `prev`, `min` with `ASSUMING ASC ID, ASC date`:

```
SELECT ID,
       min(endofdayprice - maxs(prev(endofdayprice))) AS worst_loss
FROM ticks
ASSUMING ASC ID, ASC date
GROUP BY ID
```

Example expects: s1 = -3, s2 = -60.

## (ii) Optimization

See `optimization_notes.md`.

## Run on Modal

The Modal secret `kx-license` must contain `KDB_LICENSE_B64`.

```bash
modal run example/hw1_11/run_on_modal.py
```

This builds the x86 Linux Dockerfile in Modal, deletes any previous generated q file, compiles `max_loss.a`, and executes the result with licensed q.

## Run locally with Docker

Follow the [x86-64 Linux instructions](../../aquery/docker-x86-linux/README.md).
