import mysql.connector
import pandas as pd
import os


folder_path = "excel_data"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="restaurant_db"
)
cursor = conn.cursor()


query1 = """SELECT o.item_id , m.item_name, m.category, 
m.price, count(*) as all_sales , 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income 
FROM menu_items m INNER JOIN order_details o ON m.menu_item_id = o.item_id 
GROUP BY o.item_id ORDER BY m.price * COUNT(*) DESC"""


query2 = """SELECT m.category, count(*) as all_sales, 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income 
FROM menu_items m INNER JOIN order_details o ON m.menu_item_id = o.item_id 
GROUP BY m.category ORDER BY m.price * COUNT(*) DESC"""

query3 = """SELECT o.item_id, m.item_name, m.category, m.price, 
COUNT(*) AS all_sales, 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income, 
CONCAT('$', FORMAT(m.price * COUNT(*) * 0.45, 2)) AS charges, 
CONCAT('$', FORMAT((m.price * COUNT(*)) - (m.price * COUNT(*) * 0.45), 2)) AS passive_income
FROM menu_items m 
INNER JOIN order_details o ON m.menu_item_id = o.item_id 
GROUP BY o.item_id 
ORDER BY m.price * COUNT(*) DESC"""


cursor.execute(query1)
data1 = cursor.fetchall()
df1 = pd.DataFrame(data1, columns=["Order_item_id", "item_name", "category", "price", "number_of_orders_by_item", "income"])


cursor.execute(query2)
data2 = cursor.fetchall()
df2 = pd.DataFrame(data2, columns=["category", "number_of_orders_by_item", "income"])

cursor.execute(query3)
data3 = cursor.fetchall()
df3 = pd.DataFrame(data3, columns=["Order_item_id", "item_name", "category", "price", "number_of_orders_by_item", "income" , "chargers" , "passive"])

file_path = os.path.join(folder_path, "orders_and_products.xlsx")
df4 = pd.read_excel(file_path, sheet_name="income")

sum_income_df4 = df4['income'].replace({'\$': '', ',': ''}, regex=True).astype(float).sum()
summary_data = {
    "Sheet Name": ["income"],
    "Total Income": [sum_income_df4]
}

summary_df = pd.DataFrame(summary_data)
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    df1.to_excel(writer, sheet_name="income", index=False)
    df2.to_excel(writer, sheet_name="income_by_category", index=False)
    df3.to_excel(writer, sheet_name="charges&passive", index=False)
    summary_df.to_excel(writer, sheet_name="test", index=False)


cursor.close()
conn.close()

print(f"Data has been exported to '{file_path}'")
