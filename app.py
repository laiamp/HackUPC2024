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
    
        st.components.v1.html("""
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Event Search</title>
            <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
            <script src="f_ticketmasterapi.js"></script>
        </head>
        <body>
            <input type="text" id="cityInput" placeholder="Ciudad">
            <input type="text" id="categoryInput" placeholder="Categoría">
            <input type="date" id="dataInput">
            <button id="searchEvents">Buscar Eventos</button>
            <ul id="listaEventos"></ul>
        </body>
        </html>


        """)

        js_code = """
        <script>
        $(document).ready(function() {
            $('#searchEvents').click(function() {
                var ciutat = $('#cityInput').val();
                var categoria = $('#categoryInput').val();
                var data = $('#dataInput').val();
                
                $.ajax({
                    type: "GET",
                    url: "https://app.ticketmaster.com/discovery/v2/events.json",
                    data: {
                        city: ciutat,
                        classificationName: categoria,
                        startDateTime: data + "T00:00:00Z",
                        endDateTime: data + "T23:59:59Z",
                        apikey: "YfAAYQzOHJMlfY1v9swWxAksA7dSk3YG"
                    },
                    async: true,
                    dataType: "json",
                    success: function(json) {
                        $('#listaEventos').empty(); 
                        
                        if (json._embedded && json._embedded.events && json._embedded.events.length > 0) {
                            json._embedded.events.forEach(function(evento) {
                                $('#listaEventos').append('<li>' + evento.name + '</li>');
                            });
                        } else {
                            $('#listaEventos').append('<li>No se encontraron eventos.</li>');
                        }
                    },
                    error: function(xhr, status, err) {
                        console.error("Error al obtener eventos:", err);
                    }
                });
            });
        });
        </script>"""
        st.write(js_code)
        
        #display_events(route)



    

    




