import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from staticmap import StaticMap, Line, CircleMarker


def get_graph_from_kml(filekml) -> nx.Graph:
    # Parsear el archivo KML
    G = nx.Graph()
    tree = ET.parse(filekml)
    root = tree.getroot()

    # add nodes
    # Encontrar y procesar los placemarks
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        name = placemark.findtext('{http://www.opengis.net/kml/2.2}name')
        coordinates = placemark.findtext('{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates')
        if coordinates is not None:
            coordinates = coordinates.strip().split(',')
            longitude, latitude = float(coordinates[0]), float(coordinates[1])
            print("Nombre:", name)
            print("Coordenadas (longitud, latitud):", (longitude, latitude))
            G.add_node((float(longitude), float(latitude)), name=name)


    # Encontrar y procesar los bordes (edges)
    
    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        edge_coordinates = []
        name = placemark.findtext('{http://www.opengis.net/kml/2.2}name')
        line_string = placemark.find('{http://www.opengis.net/kml/2.2}LineString')
        if line_string is not None:
            coordinates = line_string.findtext('{http://www.opengis.net/kml/2.2}coordinates')
            coordinates = coordinates.strip().split('\n')
            for coordinate in coordinates:
                coordinate = coordinate.strip().split(',')
                longitude, latitude = float(coordinate[0]), float(coordinate[1])
                edge_coordinates.append((longitude, latitude))
            
            G.add_edge(edge_coordinates[0], edge_coordinates[1])
    
    return G
  

def show(graph: nx.Graph, filename: str) -> None:
    """Export the graph to a PNG file using staticmaps."""
    map = StaticMap(1000, 1000)

    # draw nodes
    for node in graph.nodes:
        map.add_marker(CircleMarker(node, "red", 10))
        

    # draw edges
    for u, v in graph.edges:
        map.add_line(Line([u, v], "blue", 2))
    

    image = map.render()
    image.save(filename)
    image.show()


def main():
    graph = get_graph_from_kml("Eurail Map.kml")
    show(graph, "eurograf.png")


if __name__ == "__main__":
    main()
