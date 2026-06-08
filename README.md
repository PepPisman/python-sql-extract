# sql-dump-sampler

Your production DB dump is 40GB. You just want to run it locally. You don't need 10 million rows of logs to test a feature.

This script takes any MySQL dump and shrinks it down to a manageable sample — keeping the full schema, all indexes, and FK constraints intact, while capping each table at however many rows you want.

## What it does

- Reads through your `.sql` dump line by line (memory-safe, no full load)
- Keeps all `CREATE TABLE`, indexes, views, and stored procedures untouched
- Samples up to `N` rows per table from the `INSERT` statements
- Disables FK checks in the output so the import never fails
- Prints a live progress log + summary table when done

## Usage

1. Clone the repo and open `extract.py`
2. Set your paths and sample limit at the top:

```python
input_file = r"C:\path\to\your\dump.sql"
output_file = r"C:\path\to\your\dump_small.sql"
sample_limit = 50000  # rows per table
```

3. Run it:

```bash
python sampler.py
```

4. Import the output into your local DB as usual:

```bash
mysql -u root -p your_db < dump_small.sql
```

## Example output

```
→ Starting table `users`...
→ Starting table `enrollments`...
✔ Table `users` finished — 50,000 rows extracted
✔ Table `enrollments` finished — 50,000 rows extracted

 All done! Summary:
Table                                       Extracted      In Dump
------------------------------------------------------------------
users                                          50,000      834,201
enrollments                                    50,000    2,100,445
courses                                         4,821        4,821
```

## Things to know

- **FK integrity**: rows are sampled per-table independently, so FK relationships across tables aren't guaranteed to align. This is fine for local dev — the output has `SET FOREIGN_KEY_CHECKS=0` so imports work cleanly regardless.
- **Row count is approximate**: the script counts rows by scanning parentheses in `INSERT` lines. It's fast and accurate for standard mysqldump output.
- **Encoding**: reads with `errors="ignore"` so weird characters in your data won't crash it.

## Requirements

Python 3.6+ — no dependencies, stdlib only.

## License

MIT
