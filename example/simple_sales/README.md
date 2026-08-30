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

## Verify on x86-64 Linux with Modal

Run from the repository root:

```bash
modal run example/simple_sales/run_on_modal.py
```

The command builds the pinned AQuery Docker image, compiles `simple_sales.a`, runs the generated q program with KDB-X, and checks the result.

## Run with Docker

Follow the [AQuery Docker instructions](../../aquery/docker-x86-linux/README.md).

## Run without Docker

Follow the [AQuery and KDB-X course notes](../../course-materials/AQUERY_KDBX_LECTURE_NOTES.md).
