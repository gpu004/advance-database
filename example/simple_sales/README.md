# Simple AQuery sales example

This example demonstrates the complete AQuery pipeline without using a course assignment.

The input contains three rows:

```csv
item,amount
apple,3
banana,7
coffee,12
```

`simple_sales.a` loads the data and selects rows whose amount is greater than 5. The expected rows are:

```text
item    amount
banana  7
coffee  12
```

## Run with Docker

Follow the [AQuery Docker instructions](../../aquery/docker-x86-linux/README.md). The documented image works on x86-64 Linux and was also tested through Docker Desktop on an Apple M1 Mac.

## Verify the Linux control with Modal

Run from the repository root:

```bash
modal run example/simple_sales/run_on_modal.py
```

The command builds the pinned AQuery image, compiles `simple_sales.a`, runs the generated q program with KDB-X, and checks the result on x86-64 Linux.
