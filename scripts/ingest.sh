#!/bin/bash

set -e #stop kalau error

#==========================
# BASE PATH (IMPORTANT)
#==========================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"

# =========================
# CONFIG
# =========================
SOURCE_DIR="$BASE_DIR/data/source"
STAGING_DIR="$BASE_DIR/data/staging"
LOG_DIR="$BASE_DIR/data/logs"
LOG_FILE="$LOG_DIR/pipeline.log"

# FILE YANG WAJIB ADA (CRITICAL) 
REQUIRED_FILES=("Tenant.csv" "Utilities.csv" "Transactions.csv")
OPTIONAL_FILES=()
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# =========================
# INIT
# =========================

mkdir -p "$SOURCE_DIR"
mkdir -p "$STAGING_DIR"
mkdir -p "$LOG_DIR"

# =========================
# VALIDATION CEK SEMUA FILE
# =========================
echo "[$DATE] START INGESTION" >> "$LOG_FILE"
ALL_FILES_EXITS=true
for FILE in "${REQUIRED_FILES[@]}"
do
    if [ ! -f "$SOURCE_DIR/$FILE" ]; then
        echo "[$DATE] CRITICAL: $FILE missing!" >> "$LOG_FILE"
        echo "ERROR: $FILE tidak ditemukan di $SOURCE_DIR"
        ALL_FILES_EXITS=false
    fi 
done

if [ "$ALL_FILES_EXITS" = false ]; then
    echo "[$DATE] INGESTION FAILED: Missing required files" >> "$LOG_FILE"
    exit 1
fi

# ==========================
# COPY FILE KE STAGING
# ==========================
for FILE in "${REQUIRED_FILES[@]}"
do
    echo "[$DATE] Copying $FILE to staging..." >> "$LOG_FILE"
    
    # Copy ke staging (bisa pakai cp atau mv)
    cp "$SOURCE_DIR/$FILE" "$STAGING_DIR/"
    
    # Optional: Hapus dari source setelah copy (uncomment jika perlu)
    # rm "$SOURCE_DIR/$FILE"
    
    echo "[$DATE] ✓ $FILE staged successfully" >> "$LOG_FILE"
done

# ==========================
# RUN PYTHON ETL SCRIPT
# ==========================
PYTHON_SCRIPT="$BASE_DIR/etl/process.py"

if [ -f "$PYTHON_SCRIPT" ]; then
    echo "[$DATE] Running ETL process.py..." >> "$LOG_FILE"
    
    # Jalankan process.py dan capture output
    cd "$BASE_DIR"  # Pindah ke base dir agar path relatif berfungsi
    
    if python3 "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1; then
        echo "[$DATE] ETL completed successfully!" >> "$LOG_FILE"
    else
        echo "[$DATE] ETL FAILED! Check process.py" >> "$LOG_FILE"
        exit 1
    fi
else
    echo "[$DATE] ERROR: process.py not found at $PYTHON_SCRIPT" >> "$LOG_FILE"
    exit 1
fi

# ==========================
# CLEANUP STAGING (Opsional)
# ==========================
# echo "[$DATE] Cleaning staging directory..." >> "$LOG_FILE"
# rm -f "$STAGING_DIR"/*.csv

# ==========================
# FINISH
# ==========================
echo "[$DATE] END INGESTION - SUCCESS" >> "$LOG_FILE"
echo "----------------------------------------" >> "$LOG_FILE"

echo "✅ Ingestion & ETL selesai! Cek:"
echo "   - Log: $LOG_FILE"
echo "   - Output: $BASE_DIR/data/warehouse/final_dataset.csv"
echo "   - Database: industrial_db.fact_energy_usage"