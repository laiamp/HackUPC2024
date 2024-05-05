import streamlit as st
import folium
from streamlit_folium import st_folium
import json
from Utilities.templates import *
from Utilities.dataset import *
from Utilities.matches import *

route = ['Rome', 'Madrid', 'Barcelona']
categories = ['Culture', 'Gastronomy', 'Religion/Spiritual', 'Adventure/Sport', 'Rest', 'History', 'Shopping']
st.markdown("<h1 style='text-align: center;'>TravelPerk</h1>", unsafe_allow_html=True)
city_dict = get_dict()

@st.cache_data
def init_web():
    users = get_users("Data/data.csv")
    return users


if __name__ == "__main__":
    users = init_web()
    
    if 'b1' not in st.session_state:
        st.session_state.b1 = 0
        routes = []
     
                
    page = st.sidebar.selectbox("Select Page", ["Home", "SoloOption", "Shared", "EventSearcher"])


    if page == "Home":
        if st.session_state.b1 == 0:
            topics = {}
            with st.form(key ="El meu viatge"):
                name = st.text_input("Username:")
                age = st.number_input("Age:",min_value = 0, value=18, step = 1)
                idp = st.date_input("Start Date:")
                initial_date = datetime(idp.year,idp.month, idp.day)
                fdp = st.date_input("End Date:")
                final_date = datetime(fdp.year, fdp.month, fdp.day)
                flex1 = st.number_input("Flexibility before trip (days)", step = 1)
                flex2 = st.number_input("Flexibility after trip (days)", step = 1)
                city_orig = st.text_input("Start city:")
                city_dest = st.text_input("End city:")
                for c in categories:
                    topics[str(c)] = st.slider(c)
                budget = st.number_input("Budget:", step = 1)
                s = st.checkbox(label = 'Cookies')
                submitted = st.form_submit_button(label = 'Submit')

                data = (User(3000, name, age,initial_date,final_date,city_orig, city_dest,topics, budget), (timedelta(days=flex1), timedelta(days=flex2)))

            if submitted:
                st.write("Yes")
                st.session_state.b1 = 1

        if st.session_state.b1 == 1:
            st.session_state.routes = get_routes(data[0], data[1], users)
            st.divider()
            form_resume()


    if page == "SoloOption":
        vmap = render_map(st.session_state.routes[0])
        st_folium(vmap,width = 1000)
        st.divider()
        st.header("Events")
        for S in st.session_state.routes[0]:
            (urls, names) = button2(S.name, S.date)
            if urls is not None:
                st.subheader(f"{S.name} -- {S.date}")
                st.image(urls, width = 200, caption=names,use_column_width=10)
                st.divider()

    if page == "Shared":
        vmap = render_map(st.session_state.routes[1])
        st_folium(vmap,width = 1000)
        st.divider()
        st.header("Events")
        for S in st.session_state.routes[1]:
            (urls, names) = button2(S.name, S.date)
            if urls is not None:
                st.subheader(f"{S.name} -- {S.date}")
                st.image(urls, width = 200, caption=names,use_column_width=10)
                st.divider()
    
    if page == "EventSearcher":
        st.header("EventSearcher")
        button()