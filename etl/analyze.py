import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data dari database atau CSV
df = pd.read_csv('data/warehouse/final_dataset.csv')

# 1. Efficiency by Industry
plt.figure(figsize=(10,6))
sns.barplot(data=df, x='industry', y='efficiency')
plt.title('Average Efficiency by Industry')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('data/logs/efficiency_by_industry.png')
print("✅ Chart 1 saved: efficiency_by_industry.png")

# 2. Electricity vs Amount
plt.figure(figsize=(10,6))
plt.scatter(df['electricity_kwh'], df['amount'], alpha=0.5)
plt.xlabel('Electricity (kWh)')
plt.ylabel('Amount (Rp)')
plt.title('Electricity Usage vs Payment Amount')
plt.tight_layout()
plt.savefig('data/logs/electricity_vs_amount.png')
print("✅ Chart 2 saved: electricity_vs_amount.png")

print("\n📊 Analysis complete! Check data/logs/ for charts.")