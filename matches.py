import networkx as nx
from math import sqrt
import heapq
import networkx as nx
import xml.etree.ElementTree as ET
from sklearn.neighbors import KNeighborsClassifier, DistanceMetric
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    name: str
    age: int
    initial_date: datetime
    final_date: datetime
    city_orig: str
    city_dest: str
    topics: dict[str, int] 
    budget: int
    

def assign_coordenates(city):
    if city == "Paris":
        return (2.355006,48.87993)
    elif city == "Amsterdam":
        return (4.900506,52.378769)
    elif city == "Munich":
        return (11.557766,48.14045)
    elif city == "London":
        return (-0.126133,51.531427)
    elif city == "Madrid":
        return (-3.690719,40.405679)
    elif city == "Florence":
        return (11.247401,43.776565)
    elif city == "Vienna":
        return (16.376485,48.185223)
    elif city == "Zurich": 
        return (7.437358,46.948635)
    elif city == "Budapest":
        return (19.083991,47.500173)
    elif city == "Rome":
        return (12.50197,41.899798)
    elif city == "Brussels":
        return (4.357016,50.845487)
    elif city == "Dublin":
        return (-6.24715,53.352548)
    elif city == "Barcelona":
        return (2.140469,41.378603)
    elif city == "Berlin":
        return (13.369402,52.525084)
    elif city == "Prague":
        return (14.436055,50.082891)
    elif city == "Milan":
        return (9.204492,45.485641)


def intersection(user, source):
    return user.final_date >= source.initial_date  and user.initial_date < source.end_date


def filter_dates(users, source):
    return [user for user in users if intersection(user, source)]


            
def get_dates(users, dict_path_users, G):
    dates = {user: [] for user in users}
    
    # llista amb data d'arribada a cada node
    for user in users:
        cur_date = user.initial_date
        for i,node in enumerate(dict_path_users[user]):
            dates[user].append(cur_date)
            if i < len(dict_path_users[user]) - 1:
                cur_date += timedelta(hours=G[node][G.nodes[dict_path_users[user][i+1]]]["hours"])

    return dates


def travel_time(path, G):
    hours = 0

    for i in range(len(path)):
        if i < len(path) - 1:
            hours += G[path[i]][path[i+1]]["hours"]

    return hours
            


def get_joined(source, dates, dict_path_users):
    source_nodes = set(dict_path_users[source])

    joined = {}
    for user, path in dict_path_users.items():
        for i, node in enumerate(path):
            # mirem quin arriba abans
            # mirem si el que arriba abans es pot esperar
            # si pot tuto bene
            if node in source_nodes:
                if dates[user][i].date() <= dates[source][i].date():
                    waiter = user
                else:
                    waiter = source

                if dates[user][i].date() - dates[source][i].date() < travel_time(user)
                if abs() <= timedelta(days=1):
                    if user in joined:
                        joined[user].append(node)
                    else:
                        joined[user] = [node]
    
    return joined


def distance(x1, x2):
    weights = [1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 1, 1, 1]  # We adjust weights as necessary
    return sqrt(sum(((x1 - x2) * weights) ** 2))


def p_with_more_affinity(user:User, k_nearest: list[User], p:int) -> list[User]:
    min_distance = []
    for neighbor in k_nearest:
        dis = distance(user, neighbor)
        heapq.heappush(min_distance,(dis, neighbor))
    
    return [heapq.heappop(min_distance)[1] for _ in range(p)]       


def main():
    # busco gent que intersequi quant a dates
    G = nx.Graph()
    users = filter_dates(users, source)
 
    # faig path òptim per cadascú
    dict_path_users = {user: nx.dijkstra_path(G, user, user.city_orig) for user in users}
    
    dates = get_dates(users, dict_path_users, G)
    joined = get_joined(source, dates, dict_path_users)
    
    # busco si algú coincideix en algun node amb mi
    matches = p_with_more_affinity(source, list(joined.keys()), p=10)
    
    for match in matches:
        # busquem distància entre ori-dest per tots dos nodes
        # busquem totes les parelles de punts tals que
        #   dist(ori, punt1) < dist(ori,dest)
        #   dist(ori, punt1) + dist(punt2, dest) + dist(punt1,punt2) <= 1.5*dist(ori,dest)
        #   dist(punt2, dest) < dist(ori,dest)

    # donat un match fem plot dels camins. 
    # definir en quin instant comencen a anar junts
    #   si arriben en instants diferents hem d'esperar-lo i buscar activitat
    # definir en quin instant deixen d'anar junts (potser destí)


'''
Volem ajuntar rutes amb altres users
- Busquem paths òptims per tots els users cap als seus destins
- Busquem nodes comuns entre users i nou user
- Si algú s'ha desperar (hi ha delay de 2-3 dies) li busquem activitats
- Proposem activitats conjuntes al destí complementàries a l'esdeveniment target
- Recomanar activitat
- si coincideixen només en node, buscar activitat conjunta
- si coincideixen en edge, el fan junts. Si un ha d'esperar 
- calculem temps de fer viatge. El temps que pot esperar es end_date - start_date - travel.




Idees: 
- Tu t'acobles al viatge d'algú que té shortest path.
- Proposes dues rutes: una sol i una altra amb algú que faci ruta similar i tingui interessos semblats
- Tenim en compte dates
- Destins en la mateixa direcció (maybe utilitzar angles)


- if coincideixen --> aniran junts
- filtrem segons angle
'''