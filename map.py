import folium

map_path = "./europe_map.html"
if __name__ == '__main__':
    vmap = folium.Map(location = (49.20, 10.97), zoom_start= 5)
    vmap.save(map_path)
