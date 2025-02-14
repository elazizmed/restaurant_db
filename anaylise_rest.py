import mysql.connector
import pandas as pd


conn = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="", 
    database="restaurant_db"  
)


cursor = conn.cursor()


query = """SELECT o.item_id , m.item_name, m.category, 
m.price, o.order_date,o.order_time, count(*) as all_sales , 
CONCAT('$', FORMAT(m.price * COUNT(*), 2)) AS income 
FROM menu_items m INNER JOIN order_details o ON m.menu_item_id = o.item_id 
group by o.item_id ORDER BY `income` DESC """

cursor.close()
conn.close()