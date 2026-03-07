#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

# Load raw SAP export
df = pd.read_csv('sap_raw_sales.csv')

# 1. Data Cleaning
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df.dropna(subset=['Customer_ID'], inplace=True)

# 2. Retail KPI Engineering: Adding Profit Margin & Tax
df['Net_Sales'] = df['Gross_Value'] - df['Discounts']
df['Unit_Cost'] = df['Net_Sales'] * 0.7  # Simulation of COGS
df['Profit_Margin'] = df['Net_Sales'] - df['Unit_Cost']

# 3. Aggregating for Management View
mgmt_summary = df.groupby('Product_Category').agg({
    'Net_Sales': 'sum',
    'Profit_Margin': 'sum',
    'Order_ID': 'count'
}).rename(columns={'Order_ID': 'Total_Transactions'})

# Save for Power BI / MySQL Import
mgmt_summary.to_csv('cleaned_retail_data.csv')
print("Transformation Complete: Data ready for MySQL/Power BI.")


# In[ ]:




