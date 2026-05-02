#!/usr/bin/env python3
import pandas as pd
import psycopg2

# Load data
df = pd.read_csv('data/warehouse/final_dataset.csv')

print("=" * 60)
print("INDUSTRIAL ENERGY DASHBOARD")
print("=" * 60)

# 1. Basic Statistics
print("\n📊 BASIC STATISTICS:")
print(f"Total Records: {len(df):,}")
print(f"Unique Tenants: {df['tenant_id'].nunique():,}")
print(f"Date Range: {df['date'].min()} to {df['date'].max()}")
print(f"Total Revenue: Rp{df['amount'].sum():,.2f}")
print(f"Total Electricity: {df['electricity_kwh'].sum():,.0f} kWh")
print(f"Average Efficiency: {df['efficiency'].mean():.2f}")

# 2. Top 5 Industries by Revenue
print("\n🏭 TOP 5 INDUSTRIES BY REVENUE:")
industry_revenue = df.groupby('industry')['amount'].sum().sort_values(ascending=False)
for i, (industry, revenue) in enumerate(industry_revenue.head(5).items(), 1):
    print(f"  {i}. {industry}: Rp{revenue:,.2f}")

# 3. Top 5 Locations by Efficiency
print("\n📍 TOP 5 LOCATIONS BY EFFICIENCY:")
location_eff = df.groupby('location')['efficiency'].mean().sort_values(ascending=False)
for i, (location, efficiency) in enumerate(location_eff.head(5).items(), 1):
    print(f"  {i}. {location}: {efficiency:.2f}")

# 4. Bottom 5 Tenants (Need Improvement)
print("\n⚠️ TENANTS NEEDING IMPROVEMENT (Lowest Efficiency):")
bottom_tenants = df.groupby('tenant_name')['efficiency'].mean().sort_values().head(5)
for i, (tenant, efficiency) in enumerate(bottom_tenants.items(), 1):
    print(f"  {i}. {tenant[:30]}: {efficiency:.2f}")

# 5. Daily Trend
print("\n📈 DAILY TREND (Last 5 days):")
daily = df.groupby('date').agg({
    'electricity_kwh': 'sum',
    'amount': 'sum'
}).tail(5)
print(daily.to_string())

print("\n" + "=" * 60)
print("✅ Dashboard generated successfully!")