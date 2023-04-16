#!/usr/bin/env python
# coding: utf-8

# Author: Mithun Patel
# Date: 05/01/2023
# 
# Dataset: 1. restuarant.csv 2. reviews.csv
# Library: Pandas
# 
# Questions
# 1. What is the average rating for restaurants in each city?
# 2. What is the average rating for restaurants with a high price range (4 or 5) compared to restaurants with a low price range (1 or 2)?
# 3. What is the most common type of cuisine in each city?
# 4. What are the three most common types of restaurant in each country?
# 5. For each state(*correction*) City, what is the average rating for restaurants that serve Italian cuisine?
# 
# Scoping:
# - Review data for duplicates or NaNs
# - strip white space and leading commas
# - explode 'Cuisine Type' to create multiple rows
# - appropriate join, once validation of data is clean. Likely inner or right
# - update datatypes where necessary from object to string or integer
# 
# Future Scope:
# - Numpy to increase efficiency of output

# In[2]:


#import libraries for assignment
import pandas as pd


# In[3]:


#import data files, resturant + reviews, using pandas withe read_csv class
restuarant = pd.read_csv('Restaurants.csv')
reviews = pd.read_csv('Reviews.csv')


# #view top 5 entries for dataframes, size, column names, identify duplicates, and description - restuarant and review
# restuarant.head(n=5)
# reviews.duplicated('Reviewer Name').sum()
# restuarant.duplicated('Restaurant Name').sum()
# #validate duplicate 'restaurant names'
# duplicateRows1 = restuarant[restuarant.duplicated(['Restaurant Name'])]
# duplicateRows1
# #Compared restuarant with an additional column city
# duplicateRows2 = restuarant[restuarant.duplicated(['Restaurant Name', 'city'])]
# duplicateRows2
# #confirmed address and resturant are unique
# restuarant.info
# reviews.info
# restuarant.columns
# #Index(['Restaurant Name', 'address', 'city', 'country', 'Restaurant Type','Cuisine Type', 'Price Range'], dtype='object')
# reviews.columns
# #Index(['Reviewer Name', 'Restaurant Name', 'rating'], dtype='object')

# In[20]:


#upon review, observed that review dataframe, has more restuarnts than restaurant dataframe, will utilize an Inner Join versus a right join (rest on rev)
joinInner_reviewRestaurant = reviews.merge(restuarant, on='Restaurant Name', how='inner')
joinInner_reviewRestaurant['Cuisine Type'] = joinInner_reviewRestaurant['Cuisine Type'].astype(pd.StringDtype())
joinInner_reviewRestaurant['Cuisine Type'] = joinInner_reviewRestaurant['Cuisine Type'].str.strip()
joinInner_reviewRestaurant.dtypes
df = joinInner_reviewRestaurant.reindex(columns= ['Reviewer Name','Restaurant Name','Restaurant Type','city','country','address','Cuisine Type','rating','Price Range'])
df


# In[36]:


#convert datatypes to strings and Integers
df['Reviewer Name'] = df['Reviewer Name'].astype(pd.StringDtype())
df['Restaurant Name'] = df['Restaurant Name'].astype(pd.StringDtype())
df['rating'] = df['rating'].astype(int)
df['address'] = df['address'].astype(pd.StringDtype())
df['city'] = df['city'].astype(pd.StringDtype())
df['country'] = df['country'].astype(pd.StringDtype())
df['Restaurant Type'] = df['Restaurant Type'].astype(pd.StringDtype())
df['Cuisine Type'] = df['Cuisine Type'].astype(pd.StringDtype())
df['Price Range'] = df['Price Range'].astype(pd.StringDtype())
df['Cuisine Type'] = df['Cuisine Type'].str.split(",")
df.dtypes


# In[37]:


#Question 1  - What is the average rating for restaurants in each city?
Q1_dfResult = df.groupby('city')['rating'].mean()
print(Q1_dfResult)


# In[38]:


#Question 2  - What is the average rating for restaurants with a high price range (4 or 5) compared to restaurants with a low price range (1 or 2)?
columns = ['Restaurant Name','rating','Price Range']
Q2_df = pd.DataFrame(df, columns=columns)
Q2_df['dollar_value'] = Q2_df['Price Range'].str.len()
Q2_df
#df1  = df_groupbyC_q2.groupby(['rating'])['dollar_value'].mean()
Q2_dfResult  = Q2_df.groupby(['dollar_value'])['rating'].mean()
Q2_result = Q2_dfResult.to_frame()
Q2_result.dtypes
print(Q2_result.iloc[0:2, :])
print(Q2_result.iloc[3:5, :])


# Assume Dollar Value is a type of grouping, Group 2, is less expensive but has a similar cost to that of Group 4 & 5.
# There is a possibility that there is more customers spending in Group 2 than there are in Groups 4 and 5.
# Evaluating the rating, could provide a better insight to these outputs. Group 2, may be fast and more efficient.
# Whereas Group 4 and 5, may have better quality and service.
# In this example, a weighted average would provide better insight, and the rating system would need more elaboration
# for the data generating process.

# In[93]:


#Question 3  - What is the most common type of cuisine in each city?
columns = ['city','Cuisine Type']
Q3_df = pd.DataFrame(df, columns=columns)
Q3_df
#explode 'Cuisine Type' to create more rows
Q3_df1 = Q3_df.explode('Cuisine Type')
Q3_df1
#remove blanks, caused by trailing comma and dropping blanks by adding NaN
Q3_df12 = Q3_df1.replace(r'^s*$', float('NaN'), regex = True)
Q3_df12.dropna(inplace = True) 
Q3_df123 = Q3_df12.groupby(['city'])['Cuisine Type'].value_counts()
Q3_df1234 = Q3_df123.to_frame()
#The dataset contains limited data, meaning only certain cities will contain more than one Cuisine Type 
#provides a single type of cuisine in a given City.
Q3_df1234.groupby('city').head(1)


# The Dataset does not have many city with replicate values, where a count or mean can be valuable. 
# Watson Lake and some others have some variability and can play a part where TouchBistro is located geographically.
# This could also play a part in how Sales could approach similar type restuarants.

# In[85]:


#Question 4  - What are the three most common types of restaurant in each country?

columns = ['country','Restaurant Type']
Q4_df = pd.DataFrame(df, columns=columns)
#Remove commas from 'Restaurant Type'
Q4_df['Restaurant Type'] = Q4_df['Restaurant Type'].apply(lambda x: x.replace(',', ''))
#similar excercise to Question 3, grouping and counting values
Q4_df1  = Q4_df.groupby(['country'])['Restaurant Type'].value_counts()
Q4_df12 = Q4_df1.groupby('country').head(3)
Q4_df12


# Question 4, illustrates that the top most found restaurant type in the US is Buffet and Family. Easier interfaces 
# with multi-item selection for these types of Restuarants could be a feature enhancement if it does not exist today.

# In[120]:


#Question 5 - For each state(*correction*) City, what is the average rating for restaurants that serve Italian cuisine?
columns = ['country','city','Cuisine Type', 'rating']
Q5_df = pd.DataFrame(df, columns=columns)
Q5_df1 = Q5_df.explode('Cuisine Type')
Q5_df1
Q5_df12 = Q5_df1.replace(r'^s*$', float('NaN'), regex = True)
Q5_df12.dropna(inplace = True) 
Q5_df12.reset_index(drop=True, inplace=True)
Q5_df12['Cuisine Type'] = Q5_df12['Cuisine Type'].astype(pd.StringDtype())
Q5_df12['Cuisine Type'] = Q5_df12['Cuisine Type'].str.strip()
Q5_df123 = Q5_df12[Q5_df12['Cuisine Type']=='Italian']
#len(Q5_df123)
Q5_dfResult = Q5_df123.groupby('city')['rating'].mean()
Q5_dfResult


# Question 5, limited opportunity to see the .mean() play a part, as Watson Lake was the only location with multiple 
# Italian Restuarants
