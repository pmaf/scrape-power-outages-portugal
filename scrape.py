#!/usr/bin/env python3

import duckdb
import os

def append_to_parquet(url: str, file: str = "outages.parquet"):
    conn = duckdb.connect()
    conn.install_extension("httpfs")
    select_statement = "extractiondatetime as date, zipcode[1:4]::usmallint as zip4, zipcode[6:8]::usmallint as zip3"
    try:
        if os.path.exists(file):
            conn.execute(f"""
                COPY (
                    SELECT * FROM '{file}'
                    UNION SELECT {select_statement} FROM read_parquet('{url}')
                ) TO '{file}' (COMPRESSION ZSTD)
            """)
        else:
            conn.execute(f"""
                COPY (
                    SELECT {select_statement} FROM read_parquet('{url}')
                ) TO '{file}' (COMPRESSION ZSTD)
            """)
    finally:
        conn.close()

if __name__ == "__main__":
    append_to_parquet("https://e-redes.opendatasoft.com/api/explore/v2.1/catalog/datasets/outages-per-geography/exports/parquet")
