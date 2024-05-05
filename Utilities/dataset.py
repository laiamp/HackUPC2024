import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from datetime import datetime, timedelta
from Objects.User import *


def cities(df: pd.DataFrame) -> None:
    """Number of different cities and which are them"""

    cities = df["Departure City"].unique() #we have observed that arrival cities == departure cities

    #we descart Lisbon because is not connex with the other cities in Europe (once we have seen the graph)
    def_cities = [city for city in cities if city != 'Lisbon']
   
   #counts how many values of 'Lisbon' we have in the Departure City columns
    counts_dep = df['Departure City'].value_counts()
    lisbon_dep = counts_dep.get('Lisbon', 0)
    
    #counts how many values of 'Lisbon' we have in the Arrival City columns
    counts_arr = df['Arrival City'].value_counts()
    lisbon_arr = counts_arr.get('Lisbon', 0)

    
    df.loc[df['Departure City'] == 'Lisbon', 'Departure City'] = np.random.choice(def_cities, size=lisbon_dep)
    df.loc[df['Arrival City'] == 'Lisbon', 'Arrival City'] = np.random.choice(def_cities, size=lisbon_arr)

    for index, row in df.iterrows():
        if row['Departure City'] == row['Arrival City']:
            new_arrival_city = row['Arrival City']
            while new_arrival_city == row['Departure City']:
                new_arrival_city = np.random.choice(def_cities)
            df.at[index, 'Arrival City'] = new_arrival_city



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
    #num_col = interests + ['Age', 'Budget']
    #df[num_col].loc[:,:].hist(bins=20,figsize=(8,8),color='blue')
    #plt.show()


def get_users(filename) -> list[User]:
    # Read data
    df = pd.read_csv(filename, header=0, delimiter=',')
    users: list[User] = list()
    cities(df)
    dates(df)
    inputation(df)
    
    for _, row in df.iterrows():
        u: User
        topics_dict = {'Culture': row['Culture'],'Gastronomy': row['Gastronomy'],
                       'Music': row['Music'],'Architecture': row['Architecture'],
                       'Religion/Spiritual': row['Religion/Spiritual'],'Adventure/Sport': row['Adventure/Sport'], 
                       'Rest': row['Rest'],'History': row['History'],'Shopping': row['Shopping']}
        
        user = User(
            id = row["Trip ID"],
            name = row['Traveller Name'],
            age = row['Age'],
            initial_date = row['Return Date'],
            final_date = row['Return Date'],
            city_orig = row['Departure City'],
            city_dest = row['Arrival City'],
            topics = topics_dict,
            budget = row['Budget']
        )
        users.append(user)

    return users


if __name__ == "__main__":
    get_users()