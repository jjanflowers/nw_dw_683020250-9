"""Load Northwind CSV files into DuckDB raw tables without transforming them."""
import sys
from pathlib import Path

import duckdb

# ให้พิมพ์ภาษาไทยได้บน Windows ทุกรุ่น
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = ROOT / "northwind.duckdb"

# ตารางใน schema raw → ไฟล์ต้นทาง (มาจาก 2 ระบบ)
SOURCES = {
    # แหล่ง A: ระบบขายปัจจุบัน
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "orders": "raw/orders.csv",
    "order_details": "raw/order_details.csv",
    "products": "raw/products.csv",
    "shippers": "raw/shippers.csv",
    "suppliers": "raw/suppliers.csv",
    # แหล่ง B: ระบบขายเดิม (มีเฉพาะใบสั่งซื้อและรายการสินค้า)
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))
    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")
        print(f"โหลดข้อมูลเข้า {DB_PATH.name}")
        for table, relative_path in SOURCES.items():
            csv_path = DATA_DIR / relative_path
            if not csv_path.is_file():
                raise FileNotFoundError(f"ไม่พบไฟล์ {csv_path}")

            # CREATE OR REPLACE ทำ full refresh โดยคงข้อมูลจาก CSV ตามต้นฉบับ
            csv_path_sql = csv_path.as_posix().replace("'", "''")
            con.execute(
                f"""
                CREATE OR REPLACE TABLE raw.{table} AS
                SELECT *
                FROM read_csv('{csv_path_sql}', header = true)
                """
            )
            count = con.execute(f"SELECT COUNT(*) FROM raw.{table}").fetchone()[0]
            print(f" raw.{table:<22} {count:>6,} แถว")
    finally:
        con.close()

    print("เสร็จแล้ว — ขั้นต่อไป: dbt run")


if __name__ == "__main__":
    main()
