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


query2 = """SELECT m.category, 
COUNT(*) AS all_sales, 
CONCAT('$', FORMAT(SUM(m.price), 2)) AS income
FROM menu_items m
INNER JOIN order_details o ON m.menu_item_id = o.item_id
GROUP BY m.category
ORDER BY SUM(m.price) DESC;"""

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
df3 = pd.DataFrame(data3, columns=["Order_item_id", "item_name", "category", "price", "number_of_orders_by_item", "income" , "charges" , "passive"])

file_path = os.path.join(folder_path, "orders_and_products.xlsx")





if os.path.exists(file_path):

        df4 = pd.read_excel(file_path, sheet_name="all_income")
        df4['income'] = df4['income'].replace({r'\$': '', ',': ''}, regex=True)
        df4['income'] = pd.to_numeric(df4['income'], errors='coerce').fillna(0)
        sum_income_df4 = df4['income'].sum()

        df5 = pd.read_excel(file_path, sheet_name="charges&passive")
        df5['charges'] = df5['charges'].replace({r'\$': '', ',': ''}, regex=True)
        df5['charges'] = pd.to_numeric(df5['charges'], errors='coerce').fillna(0)
        sum_charges = df5['charges'].sum()

        df6 = pd.read_excel(file_path, sheet_name="charges&passive")
        df6['passive'] = df6['passive'].replace({r'\$': '', ',': ''}, regex=True)
        df6['passive'] = pd.to_numeric(df6['passive'], errors='coerce').fillna(0)
        sum_passive = df6['passive'].sum()

        summary_data = {
            "Opirations": ["income","charges","passive"],
            "Total cache": [sum_income_df4,sum_charges,sum_passive]
        }

        summary_df = pd.DataFrame(summary_data)

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
            df1.to_excel(writer, sheet_name="all_income", index=False)
            df2.to_excel(writer, sheet_name="income_by_category", index=False)
            df3.to_excel(writer, sheet_name="charges&passive", index=False)
            summary_df.to_excel(writer, sheet_name="total_income", index=False)
            print(f" the excel file aredy created !  ")
    
else:

    with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:
        df1.to_excel(writer, sheet_name="all_income", index=False)
        df2.to_excel(writer, sheet_name="income_by_category", index=False)
        df3.to_excel(writer, sheet_name="charges&passive", index=False)
        print(f" first time creating the excel file ! ")
        


cursor.close()
conn.close()

print(f"Data has been exported to '{file_path}'")
