"""Create the Northwind DuckDB database and its raw schema."""
from pathlib import Path

import duckdb

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "northwind.duckdb"


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
    finally:
        con.close()

    print(f"สร้างฐานข้อมูล {DB_PATH.name} และ schema raw แล้ว")


if __name__ == "__main__":
    main()
