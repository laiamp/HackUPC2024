import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Read data
df = pd.read_csv("data.csv", header=0, delimiter=',')
print(df.head())

#Departure cities
dep_cities = df["Departure City"].unique()
num_dep_cities = len(dep_cities)

#Arrival cities
arr_cities = df["Arrival City"].unique()
num_arr_cities = len(arr_cities)

#Total cities
cities = set(dep_cities).union(set(arr_cities))
num_cities = len(cities)

print(cities, num_cities)

#New features
interests = ['Culture', 'Gastronomy', 'Music', 'Architecture', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']
for interest in interests:
    df[interest] = np.random.randint(0, 11, size=len(df))


mu = 29  
sigma = 5  
ages = np.random.normal(mu, sigma, len(df))
adj_ages = np.clip(ages, 18, 40)
df['Age'] = adj_ages.astype(int)


mu = 85
budget = np.random.normal(mu, sigma, len(df))
adj_budget = np.clip(budget, 20, 150)
df['Budget'] = adj_budget.astype(int)


num_col = interests + ['Age', 'Budget']
df[num_col].loc[:,:].hist(bins=20,figsize=(8,8),color='blue')
plt.show()