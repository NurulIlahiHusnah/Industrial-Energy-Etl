import psycopg2
import smtplib  # untuk email alert

conn = psycopg2.connect(
    dbname="industrial_db",
    user="postgres",
    password="admin123",
    host="localhost"
)

cursor = conn.cursor()
cursor.execute("""
    SELECT COUNT(*) as total, 
           AVG(efficiency) as avg_eff
    FROM fact_energy_usage
    WHERE date = CURRENT_DATE
""")

result = cursor.fetchone()
print(f"Today's data: {result[0]} rows, Efficiency: {result[1]:.2f}")

if result[1] < 100:  # jika efisiensi rendah
    print("⚠️ Warning: Low efficiency detected!")
