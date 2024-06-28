import pandas as pd
import numpy as np
import seaborn as sns
#import missingno as msno

df = pd.read_csv('googleplaystore.csv')
df.sample(5)

## Which of the following column(s) has/have null values?
df.isna().sum().sort_values(ascending=False)

## Clean the Rating column and the other columns containing null values.
df.loc[df['Rating'] > 5, 'Rating'] = np.nan
df['Rating'].fillna(df['Rating'].mean(), inplace=True)
df.dropna(inplace=True)

## Clean the column Reviews and make it numeric.
df['Reviews Numeric'] = pd.to_numeric(df['Reviews'], errors='coerce')
df.loc[df['Reviews Numeric'].isna()]
new_reviews = (
    pd.to_numeric(df.loc[df['Reviews'].str.contains('M'), 'Reviews'].str.replace('M', '')
    ) * 1_000_000).astype(str)
new_reviews
df.loc[df['Reviews'].str.contains('M'), 'Reviews'] = new_reviews
df['Reviews'] = pd.to_numeric(df['Reviews'])

## How many duplicated apps are there?
df.loc[df.duplicated(subset=['App'], keep=False)].sort_values(by='App') # Keep false recognizes EXACT duplicates, not similar
df.duplicated(subset=['App'], keep=False).sum() # Outputs 1979

## Drop duplicated apps keeping the ones only with the greatest number of reviews.
#df_copy = df.copy()
df.sort_values(by=['App', 'Reviews'], inplace=True)
df.drop_duplicates(subset=['App'], keep='last', inplace=True)

## Format the category column to capitalize the first character and underscores to be whitespaces.
df['Category'] = df['Category'].str.replace('_', ' ')
df['Category'] = df['Category'].str.capitalize()

## Clean and convert the Installs column to numeric type by removing any + in values.
df.loc[df.to_numeric(df['Installs'], errors='coerce').isna()].nead()
df['Installs'] = pd.to_numeric(df['Installs'].str.replace('+', ' ').str.replace(",", ''))

## Clean and convert the Size column to numeric type
#df_copy = df.copy()
df.loc[df.to_numeric(df['Size'], errors='coerce').isna()].nead()
df.loc[df['Size'] == 'Varies with device', 'Size'] = pd.Series("0")
df['Size'] == df['Size'].str.replace('Varies with device', '0')

df.loc[df.['Size'].str.contains('k') 'Size'] = (
    pd.to_numeric(
        df.loc[df.['Size'].str.contains('k') 'Size'].str.replace('k', '')
    ) * 1024
).astype(str)

df.loc[df.['Size'].str.contains('M') 'Size'] = (
    pd.to_numeric(
        df.loc[df.['Size'].str.contains('M') 'Size'].str.replace('M', '')
    ) * (1024 * 1024)
).astype(str)

## Clean and convert the Price column to numeric type
df.loc[df['Price'] != '0']
df['Price'] = df['Price'].str.replace('Free', '0')
df['Price'] = pd.to_numeric(df['Price'].str.replace('$', ''))

## Paid or free?

df['Distribution'] = 'Free'
df.loc[df['Price'] > 0, 'Distribution'] = 'Paid'



# Analysis

## What company has the most reviews?
df.sort_values(by='Reviews',ascending=False).head()

## Which is the category with the most uploaded apps?
df['Category'].value_counts()

## To which category belongs the most expensive app?
df.sort_values(by='Price', ascending=False).head()

## What is the name of the most expensive game?
df.query("Category == 'Game'").sort_values(by='Price', ascending=False).head()

## Which is the most popular Finance App?
df.query("Category == 'Finance'").sort_values(by='Installs', ascending=False).head()

## What Teen Game has the most reviews?
df.query("Category == 'Game' and `Content Rating` == 'Teen'").sort_values(by='Reviews', ascending=False).head()

## What free game has the most reviews?
df.query("Category == 'Game' and Price == 0").sort_values(by='Reviews', ascending=False).head()

## How many TB were transferred overall for the most popular Lifestyle app?
app = df.query("Category == 'Lifestyle'").sort_values(by='Installs', ascending=False).iloc(0)
(app['Installs'] * app['Size']) / (1024 * 1024 * 1024 * 1024) # Outputs ~6484
