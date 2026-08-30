# AQuery and KDB-X on x86-64 Linux

## What the tools do

AQuery is a compiler. It reads an AQuery source file with the `.a` extension and generates a q program with the `.q` extension. KDB-X provides the q runtime that executes the generated program.

```text
AQuery source        AQuery compiler        q program        KDB-X
program.a      ->    a2q              ->    program.q   ->   q program.q
```

These notes use the AQuery compiler from <https://github.com/josepablocam/aquery>. Do not use the unrelated AQuery2 `prompt.py` project described in older course slides.

## Requirements

- Linux on x86-64
- A KX Community account and license
- Bash, Git, curl, gzip, unzip, and `file`
- Java for the Scala-based AQuery compiler
- No administrator access is required

Check the host:

```bash
uname -m
java -version
git --version
curl --version
unzip -v | head -1
```

`uname -m` must print `x86_64`. If Java is unavailable on the assigned NYU compute server, ask the course staff which Java module to load.

## Get a KDB-X Community license

1. Open the official KDB-X installation page: <https://code.kx.com/kdb-x/get_started/kdb-x-install.html>
2. Sign in or create a KX Developer account.
3. Obtain the base64-encoded Community license value.
4. Keep the license private. Do not place it in Git, a screenshot, lecture notes, or a shared chat.

## Clone the course setup

```bash
cd "$HOME"
git clone https://github.com/gpu004/advance-database.git
cd advance-database
```

Run the remaining installation commands from the `advance-database` repository root.

## Install KDB-X in the home directory

```bash
export KDBX_HOME="$HOME/.local/share/kdb-x"
bash aquery/image/install_kdbx.sh
source "$KDBX_HOME/env.sh"
which q
```

The script downloads the pinned x86-64 KDB-X binary, checks its SHA-256 digest, and installs q below `$HOME/.local`. It does not write to system directories.

## Install the AQuery compiler

```bash
bash aquery/image/install_aquery.sh
export PATH="$HOME/.local/bin:$PATH"
which a2q
a2q -h || true
```

The installer builds a pinned AQuery revision and writes the `a2q` launcher to `$HOME/.local/bin`.

## Store the license locally

Create a local environment file from the provided template:

```bash
cp .env.example .env
chmod 600 .env
```

Edit `.env` and replace the example value:

```env
KDB_LICENSE_B64=paste_the_complete_base64_license_value_here
```

Load the value into the current shell:

```bash
set -a
source .env
set +a
source "$KDBX_HOME/env.sh"
```

The repository ignores `.env`, but students should still confirm that it is not staged before committing:

```bash
git status --short
```

## Start q

Use the license wrapper to create a private temporary license file and start q:

```bash
aquery/image/with_kx_license.sh q
```

At the q prompt, run a smoke test:

```q
q)1+1
2
```

Enter a single backslash to exit q:

```q
q)\
```

## Run a few q queries

Create an in-memory table:

```q
q)sales:([] item:`apple`banana`coffee; amount:3 7 12)
```

Display it:

```q
q)select from sales
```

Count the rows:

```q
q)count sales
3
```

Show the items whose amount is greater than 5:

```q
q)select from sales where amount>5
```

The last query returns `banana` with amount 7 and `coffee` with amount 12. These commands demonstrate a table, a row count, and a filter.

## Compile and run the included AQuery example

Open the example directory from the repository root:

```bash
cd example/simple_sales
```

The included `sales.csv` contains:

```csv
item,amount
apple,3
banana,7
coffee,12
```

The included `simple_sales.a` query is:

```sql
CREATE TABLE sales(item STRING, amount INT)

LOAD DATA INFILE "sales.csv" INTO TABLE sales FIELDS TERMINATED BY ","

SELECT item, amount
FROM sales
WHERE amount > 5
```

Compile the AQuery file into q:

```bash
rm -f simple_sales.generated.q
a2q -c -a 1 -o simple_sales.generated.q simple_sales.a
ls -lh simple_sales.generated.q
```

Run the generated program with KDB-X:

```bash
../../aquery/image/with_kx_license.sh q simple_sales.generated.q
```

The result contains:

```text
item    amount
banana  7
coffee  12
```

The example shows the full workflow. AQuery defines and loads the table, filters the rows, generates q, and KDB-X executes the generated program.

## Run a q script

Return to the repository root:

```bash
cd ../..
```

Save the following as `hello.q`:

```q
t:([] item:`a`b`c; value:4 7 2);
show select from t where value>3;
exit 0;
```

Run it from the repository root:

```bash
source "$KDBX_HOME/env.sh"
set -a
source .env
set +a
aquery/image/with_kx_license.sh q hello.q
```

## Troubleshooting

### `q: command not found`

Reload the KDB-X environment and check the path:

```bash
source "$KDBX_HOME/env.sh"
which q
```

### License error

Confirm that `.env` contains one complete base64 value and has private permissions:

```bash
chmod 600 .env
```

Do not print the license in terminal output that will be shared.

### `a2q: command not found`

```bash
export PATH="$HOME/.local/bin:$PATH"
which a2q
```

Rerun `bash aquery/image/install_aquery.sh` if the launcher is still missing.

### Java error

Run `java -version` and record the complete error. Ask course staff which Java module the assigned compute server supports.

## References

- KDB-X installation: <https://code.kx.com/kdb-x/get_started/kdb-x-install.html>
- Introduction to q: <https://code.kx.com/kdb-x/learn/brief-introduction.html>
- Course setup: <https://github.com/gpu004/advance-database>
- AQuery source: <https://github.com/josepablocam/aquery>
- NYU CIMS access servers: <https://cims.nyu.edu/dynamic/systems/resources/accessservers/>
