import streamlit as st
import folium
from streamlit_folium import st_folium

points = [(47.50, 8), (43, 9)]
map_filepath = './europe_map.html'
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']
st.markdown("<h1 style='text-align: center;'>TravelPerk</h1>", unsafe_allow_html=True)

if 'b1' not in st.session_state:
    st.session_state.b1 = 0



def get_data():
    data = {}
    form = st.form('El meu viatge')
    data['User'] = form.text_input("Username:")
    data['Age'] = form.number_input("Age:")
    data['DI'] = form.date_input("Start Date:")
    data['DF'] = form.date_input("End Date:")
    for c in categories:
        data[str(c)] = form.slider(c)
    form.form_submit_button(label = 'Submit')
    st.session_state.form = data

def calculate_route():
    pass

def render_map():
    vmap = folium.Map(location = (49.20, 10.97), zoom_start= 5)
    #points = calculate_route()
    for point in points:
        folium.Marker(point).add_to(vmap)
    folium.PolyLine(points).add_to(vmap)
    
    st_folium(vmap)

 


            
page = st.sidebar.selectbox("Select Page", ["Home", "RouteMap", "Subpage 2"])


if page == "Home":
    if st.session_state.b1 == 0:
        if st.button("Start trip"):
            get_data()
            st.session_state.b1 = 1

if page == "RouteMap":
    render_map()
   
    




