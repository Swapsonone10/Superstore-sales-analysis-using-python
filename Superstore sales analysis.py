#!/usr/bin/env python
# coding: utf-8

# ## Superstore Sales Analysis

# In[8]:


# Importing the libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[9]:


#Importing the csv file

df = pd.read_csv("train.csv")


# In[10]:


df.head()


# In[11]:


#general overview of the data

df.info()


# In[12]:


#Calculating number of null values

null_count = df['Postal Code'].isnull().sum()
print(null_count)


# In[13]:


# filling 0 to the empty columns

df["Postal Code"].fillna(0, inplace = True)

# changing from float to integer

df["Postal Code"] = df["Postal Code"].astype(int)
df.info()


# In[14]:


df.describe()


#  ## Data Cleaning

# In[15]:


# checking for duplicates


# In[16]:


# using conditional statement
if df.duplicated().sum() > 0:
    print("Duplicates exist")
else:
    print("No duplicates exist")


# In[17]:


df.duplicated()


# In[18]:


df.duplicated(keep=False).sum()


# ## Exploratory Data Analysis

# Customer Analysis

# Customer segmentation

# In[19]:


df.head(3)


# In[20]:


# Types of customers

type_of_customers = df['Segment'].unique()
print(type_of_customers)


# In[21]:


# Number of customers in each segment

number_of_customers = df['Segment'].value_counts().reset_index()

number_of_customers = number_of_customers.rename(columns={'index':'Customer Type', 'Segment':'Total Customers'})


# In[22]:


print(number_of_customers)


# In[23]:


# Plotting a pie chart
plt.pie(number_of_customers['Total Customers'], labels=number_of_customers['Customer Type'], autopct='%1.1f%%')

# set pie chart lables
plt.title('Distribution of Customers')

plt.show()


# Customers and Sales

# In[24]:


sales_per_category = df.groupby('Segment')['Sales'].sum().reset_index()
sales_per_category = sales_per_category.rename(columns={'Segment': 'Customer Type', 'Sales': 'Total Sales'})

print(sales_per_category)


# In[25]:


# Plotting a pie chart
plt.pie(sales_per_category['Total Sales'], labels=sales_per_category['Customer Type'], autopct='%1.1f%%')

# set pie chart lables
plt.title('sales Per Customer Category')

plt.show()


# In[26]:


# Bar Graph

plt.bar(sales_per_category['Customer Type'], sales_per_category['Total Sales'] )

# Label
plt.title('Sales per Customer Category')
plt.xlabel('Customer Type')
plt.ylabel('Total Sales')

plt.show()


# ## Customer Loyalty

# In[27]:


df.head(3)


# In[28]:


# Group data according to Customer ID, Customer Name, Segment and Calculate Freq of their orders  


# In[29]:


customer_order_freq = df.groupby(['Customer ID', 'Customer Name', 'Segment'])['Order ID'].count().reset_index()

print(customer_order_freq)


# In[30]:


# Rename the Order ID column

customer_order_freq.rename(columns={'Order ID': 'Total Orders'}, inplace = True)
print(customer_order_freq)


# In[31]:


# Identify repeat customers

repeat_customers = customer_order_freq[customer_order_freq['Total Orders']>= 1]
print(customer_order_freq)


# In[32]:


# sort repeat customer in descending orders

sorted_repeat_customers = repeat_customers.sort_values(by='Total Orders', ascending=False)

print(sorted_repeat_customers.head(10))


# In[35]:


# Group data based in: Customer ID, Customer Name and Sales

customer_sales = df.groupby(['Customer ID', 'Customer Name'])['Sales'].sum().reset_index()

#sort in descending order

top_spenders = customer_sales.sort_values(by='Sales',ascending=False)

#Print the output

print(top_spenders.head(10). reset_index(drop=True))


# # Mode Of Shipping

# In[36]:


# sorting unique values in the ship mode columns into a new series

types_of_shipping = df['Ship Mode'].unique()
print(types_of_shipping)


# In[39]:


# Frequency use of shipping method

shipping_mode = df['Ship Mode'].value_counts().reset_index()
shipping_mode = shipping_mode.rename(columns={'index': 'Mode Of Shipment', 'Ship Mode': 'Use Frequency'})

print(shipping_mode)


# In[41]:


# Plotting a pie chart

plt.pie(shipping_mode['Use Frequency'], labels=shipping_mode['Mode Of Shipment'], autopct= '%1.1f%%')

# set labels
plt.title('Popular Shipping Method')

plt.show()


# # Geohraphical Analysis

# In[43]:


# Customer by states

state = df['State'].value_counts().reset_index()
state = state.rename(columns={'index':'State', 'State': 'Number of Customers'})

print(state.head(7))


# In[47]:


# Customer by city

City = df['City'].value_counts().reset_index()
City = state.rename(columns={'index':'City', 'City': 'Number of Customers'})

print(City.head(7))


# In[55]:


# Sales per State

# Grouping state and sales

state_sales = df.groupby(['State'])['Sales'].sum().reset_index()
top_state_sales = state_sales.sort_values(by='Sales', ascending=False)

# Print the top 10 states with the highest sales
print(top_state_sales.head(10).reset_index(drop=True))


# # Product Analysis

# In[56]:


df.head(3)


# In[57]:


# Types of product categories

proudcts_category = df['Category'].unique()
print(proudcts_category)


# In[60]:


# group data by product category

subcategory_count = df.groupby('Category')['Sub-Category'].nunique().reset_index()

# sort by ascending order
subcategory_count = subcategory_count.sort_values(by='Sub-Category', ascending=False)

print(subcategory_count)


# In[63]:


# Sales per each category

category_sales = df.groupby(['Category'])['Sales'].sum().reset_index()

# sort to descending order
category_sales = category_sales.sort_values(by='Sales', ascending=False)
print(category_sales.head(10).reset_index(drop=True))


# In[64]:


# Plotting a pie chart

plt.pie(category_sales['Sales'], labels=category_sales['Category'], autopct= '%1.1f%%')

# set labels
plt.title('Top Product Category Based on Sales')

plt.show()


# In[69]:


# Group data by product sub-categories vs sales
pdt_subcategory = df.groupby(['Sub-Category'])['Sales'].sum().reset_index()

# sort in descending order
top_pdt_subcategory = pdt_subcategory.sort_values(by='Sales', ascending=False)

# Print the top 10 sub-categories with the highest sales
print(top_pdt_subcategory.head(10))


# In[73]:


top_pdt_subcategory = top_pdt_subcategory.sort_values(by='Sales', ascending=True)

# Plotting the horizontal bar graph
plt.barh(top_pdt_subcategory['Sub-Category'],top_pdt_subcategory['Sales'])

# set labels
plt.title('Top Product Sub-Categories Based on Sales')
plt.xlabel('Product Sub-Categories')
plt.ylabel('Total Sales')

plt.show()


# In[76]:


# Convert order date to datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Grouping by year and summing the sales per year

yearly_sales = df.groupby(df['Order Date'].dt.year)['Sales'].sum()

# Setting a new index 

yearly_sales = yearly_sales.reset_index()
yearly_sales = yearly_sales.rename(columns={'Order Date':'Year', 'Sales': 'Total Sales'})

print(yearly_sales)


# In[77]:


# Plotting horizontal bar graph

plt.bar(yearly_sales['Year'], yearly_sales['Total Sales'])

# Label
plt.title('Yearly Sales')
plt.xlabel('Year')
plt.ylabel('Total Sales')


# In[83]:


# Plotting the line graph
plt.plot(yearly_sales['Year'], yearly_sales['Total Sales'], marker='o', linestyle='--')

# Labels
plt.title('Yearly Sales')
plt.xlabel('Year')
plt.ylabel('Total Sales')

plt.xticks(rotation=65)

plt.show()


# # Quarterly Sales

# In[88]:


# Convert order date to datetime format

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Filter data according to year
yearly_sales = df[df['Order Date'].dt.year == 2017]

# Calculate quarterly sales for year 2018
quarterly_sales = yearly_sales.resample('Q', on='Order Date')['Sales'].sum()

quarterly_sales = quarterly_sales.reset_index()
quarterly_sales = quarterly_sales.rename(columns={'Order Date': 'Quarter', 'Sales': 'Total Sales'})

print('These are the Quarterly sales for 2017')
print(quarterly_sales)


# In[92]:


# Plotting the line graph
plt.plot(quarterly_sales['Quarter'], quarterly_sales['Total Sales'], marker='o', linestyle='--')

# Labels
plt.title('Quarterly Sales')
plt.xlabel('Quarter')
plt.ylabel('Total Sales')

plt.xticks(rotation=65)

plt.show()


# # Monthly Sales Trend for a Year

# In[97]:


# Convert order date to datetime format

df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)

# Filter data according to year
year_sales = df[df['Order Date'].dt.year == 2018]

# Calculate quarterly sales for year 2018
monthly_sales = year_sales.resample('M', on='Order Date')['Sales'].sum()

monthly_sales = monthly_sales.reset_index()
monthly_sales = monthly_sales.rename(columns={'Order Date': 'Month', 'Sales': 'Total Sales'})

print('These are the Monthly sales for 2018')
print(monthly_sales)


# In[99]:


# Plotting the line graph
plt.plot(monthly_sales['Month'], monthly_sales['Total Sales'], marker='o', linestyle='--')

# Labels
plt.title('Monthly Sales')
plt.xlabel('Month')
plt.ylabel('Total Sales')

plt.xticks(rotation=65)

plt.show()


# In[ ]:




