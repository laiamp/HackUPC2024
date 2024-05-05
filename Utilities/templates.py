import streamlit as st
import folium
import json
import holidays
from Objects.User import *
from Objects.Route import *
from Objects.Map import *
import requests
import random
from Utilities.matches import *




api_key = 'YFAuf4V91WCV37YHqNXSZzsATzlEfOOI'
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']


def get_data(users):
    topics = {}
    form = st.form('El meu viatge')
    name = form.text_input("Username:")
    age = form.number_input("Age:",min_value = 0, value=18, step = 1)
    idp = form.date_input("Start Date:")
    initial_date = datetime(idp.year,idp.month, idp.day)
    fdp = form.date_input("End Date:")
    final_date = datetime(fdp.year, fdp.month, fdp.day)
    flex1 = form.number_input("Flexibility before trip (days)", step = 1)
    flex2 = form.number_input("Flexibility after trip (days)", step = 1)
    city_orig = form.text_input("Start city:")
    city_dest = form.text_input("End city:")
    for c in categories:
        topics[str(c)] = form.slider(c)
    budget = form.number_input("Budget:", step = 1)
    submitted = form.form_submit_button(label = 'Submit')

    data = (User(3000, name, age,initial_date,final_date,city_orig, city_dest,topics, budget), (timedelta(days=flex1), timedelta(days=flex2)))
    if submitted:
        routes = get_routes(data[0], data[1], users)
        return routes

def form_resume():
    st.markdown("<h2 style='text-align: center;'>My trip</h2>", unsafe_allow_html=True)

def backend():
    pass

def render_map(route):
    vmap = RMap()
    vmap.add_waypoints(route)
    vmap.draw_PolyLine(route)
    return vmap.return_map()


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
    with open('Data/f_dict_cities.txt', 'r') as file:
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

    

    if st.button("Search events"):
        # Lógica para buscar eventos y mostrarlos en la lista
        events = search_events(city_input, category_input, date_input)
        if events:
            st.markdown("### List of events")
            image_urls = []
            image_names = []
            for event in events:
                nre_images = len(event['images'])
                image_urls.append(event['images'][random.randint(0,nre_images - 1)]['url'])
                image_names.append(event['name'])
            st.image(image_urls, width = 200, caption=image_names,use_column_width=10)

        else:
            st.write("Events were not found.")



def button2(city,dat,cat = None):
    events = []
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
    else:
        st.error(f"Error al obtener eventos: {response.status_code}")

    if events:
        #st.markdown("### List of events")
        image_urls = []
        image_names = []
        for event in events:
            nre_images = len(event['images'])
            image_urls.append(event['images'][random.randint(0,nre_images - 1)]['url'])
            image_names.append(event['name'])
        return (image_urls, image_names)

    else:
        #st.write("Events were not found.")
        return (None, None)


