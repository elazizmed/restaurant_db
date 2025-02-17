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

# this query for get all income
query = """SELECT o.item_id , m.item_name, m.category, 
m.price, count(*) as all_sales , 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income 
FROM menu_items m INNER JOIN order_details o ON m.menu_item_id = o.item_id 
group by o.item_id ORDER BY `income` DESC """


#test


cursor.execute(query)

data = cursor.fetchall()
df = pd.DataFrame(data ,  columns=["Order_item_id", "item_name", "category", "price" ,"number_of_orders_by_item" , "income"] )
file_path = os.path.join(folder_path, "orders_and_products.xlsx")
df.to_excel(file_path, index=False)

cursor.close()
conn.close()

print(f"Data has been exported to '{file_path}'")