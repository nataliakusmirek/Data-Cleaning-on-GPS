# Google Play Store Data Analysis with Pandas

This project involves cleaning and analyzing data from the Google Play Store. The dataset contains information about various apps, including ratings, reviews, size, installs, and more.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Ensure you have the following packages installed:
- pandas
- numpy
- seaborn

You can install these packages using pip:

```bash
pip install pandas numpy seaborn
```

### Dataset

The dataset used in this project is `googleplaystore.csv`. Ensure the file is in the same directory as your script.

## Project Steps

### 1. Load the Data

```python
import pandas as pd
import numpy as np
import seaborn as sns

df = pd.read_csv('googleplaystore.csv')
df.sample(5)
```

### 2. Identify and Handle Missing Values

```python
df.isna().sum().sort_values(ascending=False)
df.loc[df['Rating'] > 5, 'Rating'] = np.nan
df['Rating'].fillna(df['Rating'].mean(), inplace=True)
df.dropna(inplace=True)
```

### 3. Clean and Convert Columns

#### Reviews Column

```python
df['Reviews Numeric'] = pd.to_numeric(df['Reviews'], errors='coerce')
df.loc[df['Reviews Numeric'].isna()]
new_reviews = (
    pd.to_numeric(df.loc[df['Reviews'].str.contains('M'), 'Reviews'].str.replace('M', '')) * 1_000_000).astype(str)
df.loc[df['Reviews'].str.contains('M'), 'Reviews'] = new_reviews
df['Reviews'] = pd.to_numeric(df['Reviews'])
```

#### Installs Column

```python
df['Installs'] = pd.to_numeric(df['Installs'].str.replace('+', '').str.replace(",", ''))
```

#### Size Column

```python
df.loc[df['Size'] == 'Varies with device', 'Size'] = pd.Series("0")
df['Size'] = df['Size'].str.replace('Varies with device', '0')

df.loc[df['Size'].str.contains('k'), 'Size'] = (
    pd.to_numeric(df.loc[df['Size'].str.contains('k'), 'Size'].str.replace('k', '')) * 1024).astype(str)

df.loc[df['Size'].str.contains('M'), 'Size'] = (
    pd.to_numeric(df.loc[df['Size'].str.contains('M'), 'Size'].str.replace('M', '')) * (1024 * 1024)).astype(str)
```

#### Price Column

```python
df['Price'] = df['Price'].str.replace('Free', '0')
df['Price'] = pd.to_numeric(df['Price'].str.replace('$', ''))
```

### 4. Handle Duplicate Apps

```python
df.sort_values(by=['App', 'Reviews'], inplace=True)
df.drop_duplicates(subset=['App'], keep='last', inplace=True)
```

### 5. Additional Cleaning

```python
df['Category'] = df['Category'].str.replace('_', ' ').str.capitalize()
df['Distribution'] = 'Free'
df.loc[df['Price'] > 0, 'Distribution'] = 'Paid'
```

## Analysis

### Insights

1. **Company with the most reviews**

```python
df.sort_values(by='Reviews', ascending=False).head()
```

2. **Category with the most uploaded apps**

```python
df['Category'].value_counts()
```

3. **Most expensive app and its category**

```python
df.sort_values(by='Price', ascending=False).head()
```

4. **Most expensive game**

```python
df.query("Category == 'Game'").sort_values(by='Price', ascending=False).head()
```

5. **Most popular Finance App**

```python
df.query("Category == 'Finance'").sort_values(by='Installs', ascending=False).head()
```

6. **Teen Game with the most reviews**

```python
df.query("Category == 'Game' and `Content Rating` == 'Teen'").sort_values(by='Reviews', ascending=False).head()
```

7. **Free game with the most reviews**

```python
df.query("Category == 'Game' and Price == 0").sort_values(by='Reviews', ascending=False).head()
```

8. **Total data transferred for the most popular Lifestyle app**

```python
app = df.query("Category == 'Lifestyle'").sort_values(by='Installs', ascending=False).iloc[0]
(app['Installs'] * app['Size']) / (1024 * 1024 * 1024 * 1024) # Outputs ~6484 TB
```

## What I Learned and Practiced

Through this project, I have deepened my understanding and practical skills in the following data science concepts:

- **Data Cleaning**: Identifying and handling missing values, dealing with outliers, and formatting data for analysis.
- **Data Transformation**: Converting data types, normalizing columns, and handling special cases such as units and textual data.
- **Data Deduplication**: Identifying and removing duplicate entries to ensure data integrity.
- **Exploratory Data Analysis (EDA)**: Gaining insights from data through sorting, filtering, and visualizing key metrics.
- **Data Aggregation**: Summarizing data to answer specific business questions, such as identifying top categories and most reviewed apps.
- **Pandas and NumPy Proficiency**: Utilizing powerful Python libraries for data manipulation and analysis.
