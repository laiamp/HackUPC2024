import folium
from Objects.Route import *


class RMap:
    def __init__(self, coords = (49.20, 10.97), zoom = 5):
        self.vmap = folium.Map(location=coords, zoom_start=zoom)

    @staticmethod
    def _create_waypoint(S:Stop):
        pop = f"{S.name.split(' ')[0]}: {S.partner}"
        color = 'blue'
        if S.partner is None:
            color = 'red'
            pop = S.name.split(' ')[0]
        
        M = folium.Marker((S.coords[1], S.coords[0]), 
            popup = pop,
            tooltip = str(S.date),
            icon = folium.Icon(color = color))
        return M
    
    @staticmethod
    def _create_PolyLine(Stops:list[Stop], companion):
        points = []
        if companion:
            color = "blue"
        else:
            color = "black"
        for stop in Stops:
            points.append((stop.coords[1], stop.coords[0]))
        P = folium.PolyLine(locations = points,
            color = color,
            weight = 10,
            opacity = 0.7,
            dash_array = '1, 12')
        return P
        
    
    def add_waypoints(self, R:Route):
        for S in R:
            self._create_waypoint(S).add_to(self.vmap)
        
    def draw_PolyLine(self, R:Route):
        i = 0
        while (i < len(R) - 1):
            self._create_PolyLine([R[i], R[i+1]], not ((R[i].partner is None) or (R[i+1].partner is None))).add_to(self.vmap)
            i = i + 1
            

    def return_map(self):
        return self.vmap
    




        

 
        



    