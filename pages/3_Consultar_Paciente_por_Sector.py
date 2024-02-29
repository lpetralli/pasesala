from pymongo import MongoClient
from datetime import datetime
import streamlit as st
import pandas as pd
from Funciones import mostrar_informacion
from PIL import Image

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lucaspetralliadf:probandoaustral123@micluster.tpsvtyi.mongodb.net/?retryWrites=true&w=majority&appName=micluster"

# Create a new client and connect to the server
client = MongoClient(uri, tls=True, server_api=ServerApi('1'))
db = client['Hospital']

image = Image.open('Hospital_Austral_Logo_2023.png')
st.image(image, width=100)

st.title("Sectores")

st.subheader("")

tab1, tab2, tab3 = st.tabs([":blue[TAMO]", ":blue[Abiertas]",":blue[Habitaciones]"])

with tab1:
    pacientes_tamo =  db['pacientes'].find({"sector": 'TAMO'})
    for paciente in pacientes_tamo:
        st.write(f"Nombre del paciente: {paciente['nombre']} {paciente['apellido']}")
        st.write(f"Numero de cama: {paciente['cama']}")
        boton_key = f"boton_consultar_{paciente['_id']}" 
        if st.button("Consultar paciente", key=boton_key):
            mostrar_informacion(paciente)
        st.divider()

with tab2:
    pacientes =  db['pacientes'].find({"sector": 'Abiertas'})
    for paciente in pacientes:
        st.write(f"Nombre del paciente: {paciente['nombre']} {paciente['apellido']}")
        st.write(f"Numero de cama: {paciente['cama']}")
        boton_key = f"boton_consultar_{paciente['_id']}" 
        if st.button("Consultar paciente", key=boton_key):
            mostrar_informacion(paciente)
        st.divider()

with tab3:
    pacientes =  db['pacientes'].find({"sector": 'Habitaciones'})
    for paciente in pacientes:
        st.write(f"Nombre del paciente: {paciente['nombre']} {paciente['apellido']}")
        st.write(f"Numero de cama: {paciente['cama']}")
        boton_key = f"boton_consultar_{paciente['_id']}" 
        if st.button("Consultar paciente", key=boton_key):
            mostrar_informacion(paciente)
        st.divider()


        


        

