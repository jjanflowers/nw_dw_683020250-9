"""Run a SQL query against the Northwind DuckDB database."""
import argparse
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "northwind.duckdb"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sql", help="SQL statement to run against northwind.duckdb")
    args = parser.parse_args()

    if not DB_PATH.is_file():
        raise FileNotFoundError(
            f"ไม่พบไฟล์ {DB_PATH}; รัน scripts/create_duckdb.py และ "
            "scripts/load_raw.py ก่อน"
        )

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        result = con.execute(args.sql)
        if result.description is None:
            return

        columns = [column[0] for column in result.description]
        print("\t".join(columns))
        for row in result.fetchall():
            print("\t".join("" if value is None else str(value) for value in row))
    finally:
        con.close()


if __name__ == "__main__":
    main()
