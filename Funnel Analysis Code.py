#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.graph_objects as go

# 1. Load your raw event data
# Expected columns: 'user_id', 'event_type' (e.g., view, cart, purchase), 'timestamp'
data = {
    'stage': ['Homepage', 'Product View', 'Add to Cart', 'Checkout', 'Purchase'],
    'users': [10000, 7500, 3000, 1200, 600]
}
df = pd.DataFrame(data)

# 2. Calculate Drop-off & Conversion Rates
df['conversion_rate'] = (df['users'] / df['users'].shift(1).fillna(df['users'][0]) * 100).round(2)
df['drop_off_rate'] = (100 - df['conversion_rate']).fillna(0)

# 3. Visualize the Funnel
fig = go.Figure(go.Funnel(
    y = df['stage'],
    x = df['users'],
    textinfo = "value+percent initial+percent previous"
))

fig.update_layout(title_text="E-commerce Conversion Funnel")
fig.show()

# Export for Power BI
df.to_csv('funnel_metrics.csv', index=False)


# In[ ]:




