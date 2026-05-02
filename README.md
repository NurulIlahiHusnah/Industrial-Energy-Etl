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
┌─────────────┐ ┌─────────────┐ ┌─────────────┐

│ Tenant.csv │                   │Utilities.csv│                     │Transactions │

└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
│ │ │
└────────────────┼────────────────┘
▼
┌───────────────┐
│ Staging Area │
└───────┬───────┘
▼
┌───────────────┐
│ Python ETL │
│ Load → Clean │
│Transform→Merge│
└───────┬───────┘
▼
┌───────────────┐
│ PostgreSQL │
│ Data Warehouse│
└───────┬───────┘
▼
┌───────────┴───────────┐
▼ ▼
┌─────────────┐ ┌─────────────┐
│ CSV Output │ │ Dashboard │
└─────────────┘ └─────────────┘

⏰ Cron Job: Daily at 1 AM → bash scripts/ingest.sh


---

## 🚀 Quick Start

### Prerequisites

```bash
# WSL2 (Ubuntu 22.04)
# PostgreSQL 14
# Python 3.10+
