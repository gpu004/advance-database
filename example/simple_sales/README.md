# Simple AQuery sales example

`simple_sales.a` loads three rows of sales data and selects rows where `amount > 5`.

Input:

```csv
item,amount
apple,3
banana,7
coffee,12
```

The expected rows are:

```text
item    amount
banana  7
coffee  12
```

## Run with Docker

Follow the [AQuery Docker instructions](../../aquery/docker-x86-linux/README.md). Course tests ran this image on x86 Linux and on an M1 Mac with Docker Desktop.
