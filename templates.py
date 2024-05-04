import streamlit as st

map_filepath = './europe_map.html'
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


def state():
    a = st.session_state.b1
    if (a == 0):
        if st.button("Start trip"):
            st.session_state.b1 = 1
        
    elif (a == 1):
        get_data()
        st.session_state.b1 = 0




