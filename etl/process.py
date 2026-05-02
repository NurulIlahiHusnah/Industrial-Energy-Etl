#!/usr/bin/env python3

import pandas as pd
import os
import logging
import psycopg2
from io import StringIO

# =========================
# SETUP PATH
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

STAGING_DIR = os.path.join(BASE_DIR, "data/staging")
OUTPUT_DIR = os.path.join(BASE_DIR, "data/warehouse")
LOG_DIR = os.path.join(BASE_DIR, "data/logs")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# =========================
# LOGGING
# =========================
logging.basicConfig(
    filename=os.path.join(LOG_DIR, "etl.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("ETL START")

try:
    # =========================
    # LOAD
    # =========================
    tenant = pd.read_csv(os.path.join(STAGING_DIR, "Tenant.csv"))
    usage = pd.read_csv(os.path.join(STAGING_DIR, "Utilities.csv"))
    trx = pd.read_csv(os.path.join(STAGING_DIR, "Transactions.csv"))

    logging.info("Data loaded successfully")

    # =========================
    # VALIDATION
    # =========================
    required_cols = {
        "tenant": ["tenant_id"],
        "usage": ["tenant_id", "date", "electricity_kwh"],
        "trx": ["tenant_id", "date", "amount"]
    }

    for name, df_check, cols in [
        ("tenant", tenant, required_cols["tenant"]),
        ("usage", usage, required_cols["usage"]),
        ("trx", trx, required_cols["trx"])
    ]:
        missing = [c for c in cols if c not in df_check.columns]
        if missing:
            raise ValueError(f"{name} missing columns: {missing}")

    logging.info("Validation passed")

    # =========================
    # CLEANING
    # =========================
    tenant = tenant.drop_duplicates()
    usage = usage.drop_duplicates()
    trx = trx.drop_duplicates()

    usage = usage.dropna(subset=["tenant_id", "date"])
    trx = trx.dropna(subset=["tenant_id", "date"])

    usage["electricity_kwh"] = pd.to_numeric(usage["electricity_kwh"], errors="coerce")
    trx["amount"] = pd.to_numeric(trx["amount"], errors="coerce")

    usage = usage[usage["electricity_kwh"] > 0]
    trx = trx[trx["amount"] > 0]

    logging.info("Cleaning completed")

    # =========================
    # TRANSFORM
    # =========================
    df = usage.merge(trx, on=["tenant_id", "date"], how="left")
    df = df.merge(tenant, on="tenant_id", how="left")

    df["efficiency"] = df["amount"] / df["electricity_kwh"]

    logging.info("Transformation completed")

    # =========================
    # FINAL VALIDATION
    # =========================
    if df.empty:
        raise ValueError("Final dataset is empty")

    print("Jumlah data:", len(df))

    # =========================
    # SAVE
    # =========================
    output_path = os.path.join(OUTPUT_DIR, "final_dataset.csv")
    df.to_csv(output_path, index=False)

    logging.info(f"Data saved to {output_path}")

    # =========================
    # LOAD TO POSTGRESQL
    # =========================
    conn = psycopg2.connect(
        dbname="industrial_db",
        user="postgres",
        password="admin123",  # ganti sesuai kamu
        host="localhost",
        port="5432"
    )

    cursor = conn.cursor()

    columns = list(df.columns)
    columns_str = ", ".join(columns)

    print(f"Kolom yang akan diinsert: {columns_str} dan jumlah data: {len(df)} rows ")


    buffer = StringIO()
    df.to_csv(buffer, index=False, header=True)
    buffer.seek(0)

    cursor.copy_expert(
        f"""
        COPY fact_energy_usage({columns_str})
        FROM STDIN WITH CSV HEADER 
        """,
        buffer
    )

    conn.commit()
    cursor.close()
    conn.close()

    logging.info("Data loaded to PostgreSQL")

    print("ETL selesai dengan sukses + data masuk ke database")

except Exception as e:
    logging.error(f"ETL FAILED: {str(e)}")
    print("ETL gagal, cek log untuk detail:", str(e))