import networkx as nx
import simplekml
from math import sqrt
import heapq
import networkx as nx
import xml.etree.ElementTree as ET
from sklearn.neighbors import KNeighborsClassifier, DistanceMetric

class User:
    name: str
    def __init__(self, name, age, ini_date, final_date, city_orig, city_dest, points, budget):
        self.name = name
        self.age = age
        self.initial_date = ini_date
        self.final_date = final_date
        self.city_orig = city_orig
        self.city_dest = city_dest
        self.areas = points
        self.budget = budget
    

# We convert our KML graph to NETWORKX graph
def kml_to_networkx(kml_file):
    return G

kml_file = 'archivo.kml'
graph = kml_to_networkx(kml_file)

# We select the k nearest nodes to user
def k_nearest_nodes(graph, source_node, k):
    distances = {}
    heap = [(0, source_node)]
    visited = set()

    while heap and len(distances) < k:
        distance, node = heapq.heappop(heap)
        if node not in visited:
            distances[node] = distance
            visited.add(node)
            for neighbor, weight in graph[node].items():
                new_distance = distance + weight
                if neighbor not in visited:
                    heapq.heappush(heap, (new_distance, neighbor))

    return [(node, distance) for node, distance in distances.items()]


# KNN to search among K neighbors the p ones who have more things in common

def weighted_distance(x1, x2, weights):
    return sqrt(sum(((x1 - x2) * weights) ** 2))

def custom_distance(x1, x2):
    weights = [1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 1, 1, 1]  # We adjust weights as necessary
    return weighted_distance(x1, x2, weights)
