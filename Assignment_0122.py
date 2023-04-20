
# Author: Mithun Patel
#Date: 05/01/2023

import pandas as pd

# Import data files
restaurants = pd.read_csv('Restaurants.csv')
reviews = pd.read_csv('Reviews.csv')

# Merge data frames on 'Restaurant Name'
df = reviews.merge(restaurants, on='Restaurant Name', how='inner')

# Data cleaning
df['Cuisine Type'] = df['Cuisine Type'].str.strip().str.split(',')
df['Price Range'] = df['Price Range'].astype(str).str.len()

# Question 1: Average rating for restaurants in each city
q1_df = df.groupby('city')['rating'].mean()
print(q1_df)

# Question 2: Average rating for restaurants with high/low price range
q2_df = df[['Restaurant Name', 'rating', 'Price Range']]
q2_df['Price Range'] = q2_df['Price Range'].astype(int)
q2_df['Price Category'] = pd.cut(q2_df['Price Range'], bins=[0, 2, 5], labels=['Low', 'High'])
q2_dfResult = q2_df.groupby('Price Category')['rating'].mean()
print(q2_dfResult)

# Question 3: Most common cuisine in each city
q3_df = df.explode('Cuisine Type').groupby(['city', 'Cuisine Type']).size().reset_index(name='counts')
q3_df = q3_df.sort_values(['city', 'counts'], ascending=False).groupby('city').head(1)
print(q3_df)

# Question 4: Three most common restaurant types in each country
q4_df = df.groupby(['country', 'Restaurant Type']).size().reset_index(name='counts')
q4_df = q4_df.sort_values(['country', 'counts'], ascending=False).groupby('country').head(3)
print(q4_df)

# Question 5: Average rating for Italian restaurants in each state
q5_df = df[df['Cuisine Type'].apply(lambda x: 'Italian' in x)].groupby(['state', 'city'])['rating'].mean()
print(q5_df)
