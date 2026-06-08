import re

input_file = r"C:\Users\alahm\databasedb\joacademy.sql" #copy the dump absolute path here
output_file = r"C:\Users\alahm\databasedb\joacademy_small.sql" #the output absolute path here, same as input but with _small at the end
sample_limit = 50000  # change how ever you like

insert_counts = {}
current_table = None

def count_rows_in_insert(line):
    return len(re.findall(r'\([^)]*\)', line))

def log(msg):
    print(msg, flush=True)

with open(input_file, "r", encoding="utf-8", errors="ignore") as fin, \
     open(output_file, "w", encoding="utf-8") as fout:

    for line in fin:
        if line.startswith("INSERT INTO") or line.startswith("insert into"):
            match = re.match(r"INSERT INTO `?(\w+)`?", line, re.IGNORECASE)
            if match:
                table = match.group(1)

                if table != current_table:
                    if current_table is not None:
                        written = insert_counts.get(current_table, {}).get("written", 0)
                        log(f"✔ Table `{current_table}` finished — {written:,} rows extracted")
                    current_table = table
                    if table not in insert_counts:
                        insert_counts[table] = {"written": 0, "total": 0}
                        log(f"→ Starting table `{table}`...")

                row_count = count_rows_in_insert(line)
                insert_counts[table]["total"] += row_count

                if insert_counts[table]["written"] < sample_limit:
                    fout.write(line)
                    insert_counts[table]["written"] += row_count
        else:
            fout.write(line)

    if current_table:
        written = insert_counts[current_table]["written"]
        log(f"✔ Table `{current_table}` finished — {written:,} rows extracted")

log("\n All done! Summary:")
log(f"{'Table':<40} {'Extracted':>12} {'In Dump':>12}")
log("-" * 66)
for table, counts in insert_counts.items():
    log(f"{table:<40} {counts['written']:>12,} {counts['total']:>12,}")

log(f"\nOutput saved to: {output_file}")