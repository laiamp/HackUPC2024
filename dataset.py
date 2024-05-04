import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def cities(df: pd.DataFrame) -> None:
    """Number of different cities and which are them"""

    #Departure cities
    dep_cities = df["Departure City"].unique()
    num_dep_cities = len(dep_cities)

    #Arrival cities
    arr_cities = df["Arrival City"].unique()
    num_arr_cities = len(arr_cities)

    #Total cities
    cities = set(dep_cities).union(set(arr_cities))
    num_cities = len(cities)


def dates(df: pd.DataFrame) -> None:
    """Changes the format of 'Departure Date' and 'Return Date' to datetime"""

    df['Departure Date'] = pd.to_datetime(df['Departure Date'], format='%d/%m/%Y')
    df['Return Date'] = pd.to_datetime(df['Return Date'], format='%d/%m/%Y')


def inputation(df: pd.DataFrame) -> None:
    """Inputation of new features (interests, age and budget)"""
    
    interests = ['Culture', 'Gastronomy', 'Music', 'Architecture', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']
    for interest in interests:
        df[interest] = np.random.randint(0, 11, size=len(df))


    mu = 29  #mid value between 18 and 40
    sigma = 5  
    ages = np.random.normal(mu, sigma, len(df))
    adj_ages = np.clip(ages, 18, 40)
    df['Age'] = adj_ages.astype(int)


    mu = 85 #mid value between 20 and 150
    budget = np.random.normal(mu, sigma, len(df))
    adj_budget = np.clip(budget, 20, 150)
    df['Budget'] = adj_budget.astype(int)


    #Plot distributions
    num_col = interests + ['Age', 'Budget']
    df[num_col].loc[:,:].hist(bins=20,figsize=(8,8),color='blue')
    plt.show()


def main():
    # Read data
    df = pd.read_csv("data.csv", header=0, delimiter=',')
    dates(df)
    inputation(df)

    print(df.head())


if __name__ == "__main__":
    main()