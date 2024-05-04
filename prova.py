import streamlit as st
from Objects.Route import *
from Objects.Map import *
from streamlit_folium import st_folium



st.title('Prova')



city_list = ['Barcelona', 'Paris', 'Berlin']
coord_list = [[41.378603, 2.140469],[48.87993, 2.355006], [52.525084, 13.369402]]

if __name__ == "__main__":
    R = create_route(city_list, coord_list)
    M = RMap()
    M.add_waypoints(R)
    M.draw_PolyLine(R)
    vmap = M.return_map()
    st_folium(vmap)
    
