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
GROUP BY o.item_id ORDER BY `income` DESC"""


query2 = """SELECT m.category, count(*) as all_sales , 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income 
FROM menu_items m INNER JOIN order_details o ON m.menu_item_id = o.item_id 
GROUP BY m.category ORDER BY `income` DESC"""


cursor.execute(query1)
data1 = cursor.fetchall()
df1 = pd.DataFrame(data1, columns=["Order_item_id", "item_name", "category", "price", "number_of_orders_by_item", "income"])

cursor.execute(query2)
data2 = cursor.fetchall()
df2 = pd.DataFrame(data2, columns=["category", "number_of_orders_by_item", "income"])


file_path = os.path.join(folder_path, "orders_and_products.xlsx")
with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
    df1.to_excel(writer, sheet_name="income", index=False)
    df2.to_excel(writer, sheet_name="income_by_category", index=False)


cursor.close()
conn.close()

print(f"Data has been exported to '{file_path}'")
