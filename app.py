import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from templates import *

route = ['Rome', 'Madrid', 'Barcelona']
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']
st.markdown("<h1 style='text-align: center;'>TravelPerk</h1>", unsafe_allow_html=True)
city_dict = get_dict()


if __name__ == "__main__":
    if 'b1' not in st.session_state:
        st.session_state.b1 = 0
                
    page = st.sidebar.selectbox("Select Page", ["Home", "RouteMap", "Subpage 2"])


    if page == "Home":
        if st.session_state.b1 == 0:
            if st.button("Start trip"):
                get_data()
                st.session_state.b1 = 1


    if page == "RouteMap":
        #route= calculate_route()
        vmap = render_map(route,city_dict)
        st_folium(vmap)
        #display_events(route['cities'])
        html_file_url = './pag.html'
        button()
        #display_events(route)
