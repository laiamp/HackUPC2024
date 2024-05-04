import streamlit as st
import folium
import json
import holidays

api_key = 'YFAuf4V91WCV37YHqNXSZzsATzlEfOOI'
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']

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

def render_map(route, city_dict):
    vmap = folium.Map(location = (49.20, 10.97), zoom_start= 5)
    points = []
    for city in route: 
        points.append(city_dict[str(city)])
    
    for point in points:
        folium.Marker(point).add_to(vmap)
    folium.PolyLine(points).add_to(vmap)
    return vmap

def display_connections(points):
    pass


def display_events(cities):
    st.subheader("Events")
    route_point = st.selectbox("Select where to explore events", cities)
    events = api_call(route_point, st.session_state.form['DF'])
    st.table(events.events)


@st.cache_data
def api_call(city, date):
    tz = 'Madrid' + "/Europe"
    dte = str(date)
    client = holidays.client(api_key)
    events = client.getEvents()#timezone=tz, date=dte)
    return events



@st.cache_data
def get_dict():
    with open('f_dict_cities.txt', 'r') as file:
        data = file.read()
        dictionary = json.loads(data)
    return dictionary




