import networkx as nx
from math import sqrt
import heapq
import networkx as nx
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import TypeAlias

from eurotrain import *

@dataclass(frozen=True)
class Stop:
    name: str
    coords: tuple[float,float]
    event: bool
    date: datetime
    partner: str

Route: TypeAlias = list[Stop]



@dataclass(frozen=True)
class User:
    id: int
    name: str
    age: int
    initial_date: datetime
    final_date: datetime
    city_orig: str
    city_dest: str
    topics: dict[str, int] 
    budget: int    

def coordinates(city):
    if city == "Paris":
        return (2.355006,48.87993)
    elif city == "Amsterdam":
        return (4.900506,52.378769)
    elif city == "Munich":
        return (11.557766,48.140458)
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


def intersection(user, source, flex):
    return user.final_date >= source.initial_date- flex[0]  and user.initial_date < source.final_date + flex[1]


def filter_dates(users, source, flex):
    return [user for user in users if intersection(user, source, flex)]


def get_dates(users, dict_path_users):
    dates = {}

    # per cada user miro el seu path
    # per cada path miro els seus nodes
    for user in users:
        date = user.initial_date
        for i in range(len(dict_path_users[user.id])):
            if user.id not in dates:
                dates[user.id] = [date.date()]
            else:
                dates[user.id].append(date.date())

            date += timedelta(days=1)

    return dates

    

def get_joined(source:User, dates, dict_path_users):
    source_nodes = set(dict_path_users[source.id])

    joined = {}
    for id, path in dict_path_users.items():
        if id != source.id:
            for i, node in enumerate(path):
                if node in source_nodes:
                    if id in joined:
                        joined[id].append((node, dates[id][i]))
                    else:
                        joined[id] = [(node, dates[id][i])]
            
    return joined


def distance(u1, u2):
    
    weights = [1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 1, 1, 1]  # We adjust weights as necessary
    return sum(((u1.topics[topic] - u2.topics[topic]) * weights[i]) ** 2 for i,topic in enumerate(u1.topics.keys()))


def p_with_more_affinity(user: User, k_nearest: list[User], p:int) -> list[User]:
    min_distance = []
    for neighbor in k_nearest:
        dis = distance(user, neighbor)
        heapq.heappush(min_distance,(dis, neighbor.id))
    
    p_matches = [heapq.heappop(min_distance)[1] for _ in range(p)]
    return [u for u in k_nearest if u.id in p_matches]       



def get_routes(root, flex, users) -> list[Route]:
    # busco gent que intersequi quant a dates
    G = get_graph_from_kml("Eurail Map.kml")
    users = filter_dates(users, root, flex) # done (té en compte flexibility)
    all_users = users + [root]
    # faig path òptim per cadascú
    dict_path_users: dict[User, list[nx.node]] = {user.id: nx.dijkstra_path(G, coordinates(user.city_orig), coordinates(user.city_dest)) for user in all_users}
    dates: dict[User, list[datetime]] = get_dates(all_users, dict_path_users)
    joined: dict[User, list[tuple[nx.node, datetime]]] = get_joined(root, dates, dict_path_users)
    matches = p_with_more_affinity(root, [user for user in users if user.id in joined.keys()], p=10)
    
   
    routes = [[Stop(G.nodes[dict_path_users[root.id][i]]["name"], node, i == len(dict_path_users) - 1, dates[root.id][i], None) for i, node in enumerate(dict_path_users[root.id])]]


    for match in matches:
        node, data_match = joined[match.id][0]
        route = []
        # same day
        if data_match == dates[root.id][dict_path_users[root.id].index(node)]:
            # afegeix tots els nodes de path
            # des de 0 fins a node - 1 --> None
            # des de node fins a dict_path_users[root].index(node)
            for i in range(len(dict_path_users[root.id])):
                name = G.nodes[dict_path_users[root.id][i]]["name"]
                coord = dict_path_users[root.id][i]
                event = False if i < len(dict_path_users[root.id]) - 1 else True
                date = dates[root.id][i]
                partner = match.name if dict_path_users[root.id].index(node) <= i <= dict_path_users[root.id].index(joined[match.id][-1][0]) else None

                route.append(Stop(name,coord,event,date,partner))
            
            routes.append(route)
            print("atope tenim match perfecte!!")

        elif dates[root.id][dict_path_users[root.id].index(node)] - data_match <=  flex[0]: 
            
            for i in range(len(dict_path_users[root.id])):
                name = G.nodes[dict_path_users[root.id][i]]["name"]
                coord = dict_path_users[root.id][i]
                event = False if i < len(dict_path_users[root.id]) - 1 else True
                date = dates[root.id][i] - (dates[root.id][dict_path_users[root.id].index(node)] - data_match)
                
                partner = match.name if dict_path_users[root.id].index(node) <= i <= dict_path_users[root.id].index(joined[match.id][-1][0]) else None

                route.append(Stop(name,coord,event,date,partner))
            
            routes.append(route)
            
            print(f'them davançar {"X"} dies')


        elif data_match - dates[root.id][dict_path_users[root.id].index(node)] <= flex[1]: # arribo abans
            # atrassem
            print(f'them datrassar {"X"} dies')
            for i in range(len(dict_path_users[root.id])):
                name = G.nodes[dict_path_users[root.id][i]]["name"]
                coord = dict_path_users[root.id][i]
                event = False if i < len(dict_path_users[root.id]) - 1 else True
                date = dates[root.id][i] + (data_match - dates[root.id][dict_path_users[root.id].index(node)])
                partner = match.name if dict_path_users[root.id].index(node) <= i <= dict_path_users[root.id].index(joined[match.id][-1][0]) else None

                route.append(Stop(name,coord,event,date,partner))
            
            routes.append(route)

            route = []
            print("podem buscar-te activitats per dies X")
            for i in range(len(dict_path_users[root.id])):
                
                dict_path_users[root.id][i]
                name = G.nodes[dict_path_users[root.id][i]]["name"]
                coord = dict_path_users[root.id][i]
                event = False if i < len(dict_path_users[root.id]) - 1 else True
                date = dates[root.id][i]
                partner = match.name if dict_path_users[root.id].index(node) <= i <= dict_path_users[root.id].index(joined[match.id][-1][0]) else None
                if dict_path_users[root.id][i] == node:
                    for _ in range((data_match - dates[root.id][dict_path_users[root.id].index(node)]).days):
                        route.append(Stop(name,coord,event,date,partner))
                else:
                    route.append(Stop(name,coord,event,date,partner))
            
            routes.append(route)


    return routes 


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

'''