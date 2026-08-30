# Simple AQuery sales example

Three rows of sales data and one `amount > 5` filter.

Input:

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

Follow the [AQuery Docker instructions](../../aquery/docker-x86-linux/README.md). The documented image works on x86 Linux and was also tested with Mac M-series Docker on an M1 Mac.
