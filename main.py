import pandas as pd
import sqlite3

# Load CSV data
df = pd.read_csv("data/sales_data.csv")

# Create database connection
conn = sqlite3.connect("database.db")

# Store data into SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)

# SQL query: Total sales per person
query = """
SELECT Name, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Name
"""

result = pd.read_sql(query, conn)

print("Sales Summary:")
print(result)


query2 = """
SELECT Product, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Product
ORDER BY Total_Sales DESC
"""

product_result = pd.read_sql(query2, conn)

print("\nTop Products:")
print(product_result)

query3 = """
SELECT Name, SUM(Sales) as Total_Sales
FROM sales
GROUP BY Name
ORDER BY Total_Sales DESC
LIMIT 1
"""

top_person = pd.read_sql(query3, conn)

print("\nTop Performer:")
print(top_person)

conn.close()

import matplotlib.pyplot as plt

# Bar chart for product sales
product_result.plot(x="Product", y="Total_Sales", kind="bar")

plt.title("Product Sales Distribution")
plt.xlabel("Product")
plt.ylabel("Total Sales")

plt.savefig("product_sales_chart.png")

print("\nChart generated successfully 📊")

# Save results to Excel
with pd.ExcelWriter("analysis_report.xlsx") as writer:
    result.to_excel(writer, sheet_name="Sales Summary", index=False)
    product_result.to_excel(writer, sheet_name="Product Sales", index=False)
    top_person.to_excel(writer, sheet_name="Top Performer", index=False)

print("Excel report generated successfully 📁")