import streamlit as st
import folium
import json
import holidays
from Objects.User import *
from Objects.Route import *
import requests




api_key = 'YFAuf4V91WCV37YHqNXSZzsATzlEfOOI'
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']

def get_data():
    data = User()
    form = st.form('El meu viatge')
    User.name = form.text_input("Username:")
    User.age = form.number_input("Age:")
    User.initial_date = form.date_input("Start Date:")
    User.final_date = form.date_input("End Date:")
    User.city_orig = form.text_input("Start city:")
    User.city_dest = form.text_input("End city:")

    for c in categories:
        User.topics[str(c)] = form.slider(c)
    form.form_submit_button(label = 'Submit')
    st.session_state.form = data

def backend():
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


def button():
    def search_events(city, cat, dat):
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        params = {
            "city": city,
            "classificationName": cat,
            "startDateTime": f"{dat}T00:00:00Z",
            "endDateTime": f"{dat}T23:59:59Z",
            "apikey": "YfAAYQzOHJMlfY1v9swWxAksA7dSk3YG"
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            events = data.get("_embedded", {}).get("events", [])
            return events
        else:
            st.error(f"Error al obtener eventos: {response.status_code}")

            
    city_input = st.text_input("City")
    category_input = st.text_input("Category", "")
    date_input = st.date_input("Date")

    st.title("Event Search")

    if st.button("Search events"):
        # Lógica para buscar eventos y mostrarlos en la lista
        events = search_events(city_input, category_input, date_input)
        if events:
            st.markdown("### List of events")
            for event in events:
                st.write(event['name'])
                nre_images = st.image(event['images']).len()
                st.image(event['images'][random.randint(nre_images)]['url'], caption='Imatge', use_column_width=True)
                st.write(event['images'][0]['ratio'])
                st.write(event['images'][0]['fallback'])


        else:
            st.write("Events were not found.")




