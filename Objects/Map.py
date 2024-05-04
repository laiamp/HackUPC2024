import folium
from Objects.Route import *


class RMap:
    def __init__(self, coords = (49.20, 10.97), zoom = 5):
        self.vmap = folium.Map(location=coords, zoom_start=zoom)

    @staticmethod
    def create_waypoint(S:Stop):
        color = 'blue'
        if S.partner is None:
            color = 'red'
        M = folium.Marker(S.coords, 
            popup = S.name,
            tooltip = str(S.date),
            icon = folium.Icon(color = color))
        return M
    
    @staticmethod
    def create_PolyLine(Stops:list(Stop)):
        if Stops[0].partner is None:
            color = 'black'
        else:
             color = 'blue'

        points = []
        for stop in Stops:
            points.append(stop.coords)
        P = folium.PolyLine(locations = points,
            color = color,
            weight = 5,
            opacity = 0.7,
            dash_array = '5, 5')
        return P
        
    
    def add_waypoints(self, R:Route):
        for S in R:
            self.create_waypoint(S).add_to(self.vmap)
        
    def draw_PolyLine(self, R:Route):
        i = 1
        line = [R[0]]
        while (i < len(R)):
            if R[i].partner == R[i - 1].partner:
                line.append(R[i])
            else:
                self.create_PolyLine(line).add_to(self.vmap)
            i = i + 1
    def return_map(self):
        return self.vmap
    




        

 
        



    