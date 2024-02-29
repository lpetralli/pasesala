from pymongo import MongoClient
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image
from Funciones import mostrar_informacion, modificar_valor, agregar_informacion

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lucaspetralliadf:4cgH0uxNSnfOGtr3@pruebahua.olbttjo.mongodb.net/?retryWrites=true&w=majority&appName=pruebaHUA"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Hospital']

image = Image.open('Hospital_Austral_Logo_2023.png')
st.image(image, width=100)

st.title("Vista Paciente") 

df = pd.DataFrame(
    {
        "Información": ["Camila Lopez", "E: 20", "P: 50"],
        "Medicacion": ["amoxidal 20mg", "gotas para ojos 50mg", "nada 0 mg"],
        "Plan Accion": ["hola", "chau", "hola"],
        "Contingencia": ["hola", "chau", "hola"]
    }
)

st.dataframe(
    df,
    column_config={
        "Información": "App name",
        "Medicacion": "Medicacion",
        "Plan Accion": "Plan accion",
        "Contingencia": "Contingencia"

    },
    hide_index=True,
)