import csv

with open("sales.csv", newline="") as file:
    rows = csv.DictReader(file)
    total = sum(int(row["revenue"]) for row in rows)

print(f"Total revenue: {total}")
