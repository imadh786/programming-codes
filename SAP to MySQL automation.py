#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#The architecture to automate reporting from SAP Business One (SAP B1) and E-commerce platform.
# For this I will implement ETL(Extract, Transform & Load) pipeline that centralizes data in a Data Warehouse(Mysql) or SSOT before visualizing. 

#Extraction:
#This template provides two common ways to extract data from SAP Business One (SAP B1): via the Service Layer (REST API)—which is the most flexible for modern automation—and direct Database Connection (SQL Server or HANA) for high-volume extraction.

#Option 1: Using SAP B1 Service Layer 
#This method uses standard HTTP requests to fetch data as JSON, which is ideal for real-time extraction without needing direct database access.

import requests
import pandas as pd

# 1. Connection Settings
BASE_URL = "https://<your-server-address>:50000/b1s/v1"
LOGIN_PAYLOAD = {
    "CompanyDB": "YOUR_COMPANY_DB",
    "UserName": "YOUR_USERNAME",
    "Password": "YOUR_PASSWORD"
}

# 2. Login to get Session ID (Bearer Token)
login_response = requests.post(f"{BASE_URL}/Login", json=LOGIN_PAYLOAD, verify=False)
session_id = login_response.json().get('SessionId')

# 3. Extract Data (e.g., Sales Orders)
headers = {'Cookie': f'B1SESSION={session_id}'}
# Use $select to get specific columns and $filter for real-time/recent data
query_url = f"{BASE_URL}/Orders?$select=DocEntry,DocNum,CardCode,DocTotal&$filter=DocDate ge '2024-01-01'"

data_response = requests.get(query_url, headers=headers, verify=False)
orders_df = pd.DataFrame(data_response.json()['value'])

print(orders_df.head())


# In[ ]:


#If SAP B1 runs on SQL Server, pyodbc library will be used. If it runs on SAP HANA, hdbcli library will be used. 

#For SQL Server (MSSQL):

import pyodbc
import pandas as pd

# Connection string for SQL Server
conn_str = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=YOUR_SERVER_IP;"
    "DATABASE=YOUR_COMPANY_DB;"
    "UID=YOUR_SQL_USER;"
    "PWD=YOUR_SQL_PASSWORD"
)

# Extract using SQL Query
query = "SELECT DocEntry, DocNum, CardCode, DocTotal FROM ORDR WHERE DocDate >= '2024-01-01'"
with pyodbc.connect(conn_str) as conn:
    df_sap = pd.read_sql(query, conn)

print(df_sap.head())


# In[ ]:


#For SAP HANA, hdbcli library will be used.

from hdbcli import dbapi
import pandas as pd

# Connect to HANA Database
conn = dbapi.connect(
    address="YOUR_HANA_HOST",
    port=30015, # 30015 for single-tenant, check your instance
    user="YOUR_USER",
    password="YOUR_PASSWORD"
)

query = "SELECT \"DocEntry\", \"DocNum\", \"CardCode\", \"DocTotal\" FROM ORDR"
df_hana = pd.read_sql(query, conn)
print(df_hana.head())


# In[ ]:


#Defining the DataFrames(orders_df or df_SAP) before loading to My Sql and then establishing the connection using sqlalchemy.

#Depending on the source (standard orders or an SAP-style export), can create your DataFrame as follows:
#Option A: Standard orders_df

import pandas as pd

# Creating a sample orders DataFrame
data_orders = {
    'order_id': [101, 102, 103],
    'customer_id': [1, 2, 1],
    'order_date': pd.to_datetime(['2023-10-01', '2023-10-02', '2023-10-02']),
    'total_amount': [150.50, 200.00, 50.25],
    'status': ['Shipped', 'Pending', 'Shipped']
}
orders_df = pd.DataFrame(data_orders)


# In[ ]:


#Option B: SAP-Style df_sap:

data_sap = {
    'VBELN': ['00100001', '00100002', '00100003'], # Sales Document
    'ERDAT': ['20231001', '20231002', '20231003'], # Creation Date
    'KUNNR': ['00001234', '00005678', '00001234'], # Customer Number
    'NETWR': [1500.00, 2200.50, 450.00],          # Net Value
    'WAERK': ['USD', 'EUR', 'USD']                # Currency
}
df_sap = pd.DataFrame(data_sap)

# 2. Configure Database Credentials
USER = 'your_username'
PASSWORD = 'your_password'
HOST = 'localhost' # or your server IP
PORT = '3306'
DB_NAME = 'reporting_db'




# In[ ]:


# 3. Create SQLAlchemy Engine
# Format: mysql+pymysql://<user>:<password>@<host>:<port>/<dbname>

connection_string = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
engine = create_engine(connection_string)

# 4. Automate the Transfer

try:
    # Use if_exists='replace' to overwrite or 'append' to add to existing data

    df_sap.to_sql(name='sap_sales_reporting', con=engine, if_exists='replace', index=False)
    print("Transfer successful: df_sap moved to MySQL.")
except Exception as e:
    print(f"Transfer failed: {e}")
finally:
    # Optional: Dispose the engine to free resources
    engine.dispose()


# In[ ]:




