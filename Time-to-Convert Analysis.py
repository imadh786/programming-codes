#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# 1. Prepare your event data
# Requirements: Columns ['user_id', 'event_type', 'timestamp']
# 'timestamp' must be in datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'])

# 2. Pivot the data to create a user-centric timeline
funnel_df = df.pivot(index='user_id', columns='event_type', values='timestamp')

# 3. Calculate time differences (Example: View -> Cart and Cart -> Purchase)
# We calculate total_seconds() for easier aggregation
funnel_df['view_to_cart_sec'] = (funnel_df['add_to_cart'] - funnel_df['product_view']).dt.total_seconds()
funnel_df['cart_to_purchase_sec'] = (funnel_df['purchase'] - funnel_df['add_to_cart']).dt.total_seconds()

# 4. Extract Key Insights
# Use median to find the "typical" user experience
conversion_speed = {
    "Median Sec to Cart": funnel_df['view_to_cart_sec'].median(),
    "Median Sec to Purchase": funnel_df['cart_to_purchase_sec'].median(),
    "Max Sec to Purchase": funnel_df['cart_to_purchase_sec'].max()
}

print(conversion_speed)

# 5. Segment for Power BI
# Keep only the time metrics for export
final_export = funnel_df[['view_to_cart_sec', 'cart_to_purchase_sec']].dropna()
final_export.to_csv('time_to_convert.csv')


# In[ ]:




