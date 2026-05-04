# 🏭 Industrial Energy ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 📌 Overview

Automated ETL pipeline untuk memproses data energi industri dari 3 sumber berbeda (Tenant, Utilities, Transactions) hingga siap analisis di data warehouse.

**Hasil:** Pipeline otomatis memproses **1.000+ records** dari **500+ tenant** industri dengan scheduling harian.

---

## 🎯 Business Impact

- ✅ Mengidentifikasi **Top 5 industri** dengan revenue tertinggi
- ✅ Menemukan **10 tenant prioritas** dengan efisiensi terendah (perlu improvement)
- ✅ Menyediakan metrik **efisiensi energi** (revenue per kWh)
- ✅ Mengurangi waktu laporan manual dari **berjam-jam menjadi < 5 detik**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Extract** | CSV files (Pandas) |
| **Transform** | Python (Pandas, NumPy) |
| **Load** | PostgreSQL 14 |
| **Orchestration** | Bash Scripting |
| **Scheduling** | Cron Job |
| **Environment** | WSL2 (Ubuntu 22.04) |

---

## 📊 Architecture
![Architecture] Arsitecture Diagram.png

⏰ Cron Job: Daily at 1 AM → bash scripts/ingest.sh


---

## 🚀 Quick Start

### Prerequisites

```bash
# WSL2 (Ubuntu 22.04)
# PostgreSQL 14
# Python 3.10+
```

# Clone repository
```bash
git clone https://github.com/NurulIlahiHusnah/industrial-energy-etl.git
cd industrial-energy-etl
```
# Install Python dependencies
```pip install -r requirements.txt```

# Setup PostgreSQL
```bash
sudo -u postgres psql -c "CREATE DATABASE industrial_db;"
psql -U postgres -d industrial_db -f schema.sql```

# Run Python script directly
```bash
python3 etl/process.py```

# Or run full pipeline with orchestrator
bash scripts/ingest.sh

# Add to crontab (runs daily at 1 AM)
crontab -e
# Add line: 0 1 * * * cd /path/to/project && bash scripts/ingest.sh

-- Top 5 industries by revenue
SELECT industry, SUM(amount) as revenue
FROM fact_energy_usage
GROUP BY industry
ORDER BY revenue DESC
LIMIT 5;

   industry    |   revenue    
---------------+--------------
 Manufacturing | Rp45,234,567
 Tech          | Rp32,123,456
 Energy        | Rp28,765,432
