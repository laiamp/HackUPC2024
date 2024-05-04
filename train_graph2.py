from math import sqrt
import heapq
import networkx as nx

class User:
    name: str
    def __init__(self, name, age, ini_date, final_date, city_orig, city_dest, points, budget):
        self.name = name
        self.age = age
        self.initial_date = ini_date
        self.final_date = final_date
        self.city_orig = city_orig
        self.city_dest = city_dest
        self.topics = points
        self.budget = budget


# KNN to search among K neighbors the p ones who have more things in common
def weighted_distance(x1, x2, weights):
    return sqrt(sum(((x1 - x2) * weights) ** 2))

def custom_distance(x1, x2):
    weights = [1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 1, 1, 1]  # We adjust weights as necessary
    return weighted_distance(x1, x2, weights)

def p_with_more_affinity(user:User, k_nearest: list[User], p:int) -> list[User]:
    min_distance = []
    for neighbor in k_nearest:
        dis = custom_distance(user, neighbor)
        heapq.heappush(min_distance,(dis, neighbor))
    
    return [heapq.heappop(min_distance)[1] for _ in range(p)]



