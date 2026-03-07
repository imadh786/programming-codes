#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import mysql.connector
import time

# 1. Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="your_user",
    password="your_password",
    database="reporting_sales"
)
cursor = db.cursor()

def poll_orders():
    # 2. Get the last order ID from your MySQL to avoid duplicates
    cursor.execute("SELECT MAX(order_id) FROM orders")
    last_id = cursor.fetchone()[0] or 0

    # 3. Call the API
    url = f"https://api.jumbosouq.com{last_id}"
    headers = {"Authorization": "Bearer YOUR_API_TOKEN"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        orders = response.json()
        for order in orders:
            # 4. Insert into MySQL Staging Table
            sql = "INSERT INTO stage_orders (order_id, amount, status) VALUES (%s, %s, %s)"
            cursor.execute(sql, (order['id'], order['total'], order['status']))
        db.commit()
        print(f"Synced {len(orders)} new orders.")

# 5. Run every 10 minutes
while True:
    poll_orders()
    time.sleep(600) 


# In[ ]:




