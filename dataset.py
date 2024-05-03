import pandas as pd

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



