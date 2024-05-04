import networkx as nx
import simplekml


# We convert our KML graph to NETWORKX graph
def kml_to_networkx(kml_file):
    G = nx.Graph()

    kml = simplekml.Kml()
    kml_file_content = open(kml_file, 'r').read()
    kml.from_string(kml_file_content)

    for placemark in kml.features():
        if isinstance(placemark.geometry, simplekml.Point):
            coords = (placemark.geometry.coordinates[0], placemark.geometry.coordinates[1])
            G.add_node(coords)

    for placemark in kml.features():
        if isinstance(placemark.geometry, simplekml.LineString):
            coords = [(point[0], point[1]) for point in placemark.geometry.coords]
            for i in range(len(coords)-1):
                G.add_edge(coords[i], coords[i+1])

    return G

kml_file = 'archivo.kml'
graph = kml_to_networkx(kml_file)