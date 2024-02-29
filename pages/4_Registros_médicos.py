from pymongo import MongoClient
import streamlit as st
from PIL import Image
from Funciones import mostrar_informacion

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://lucaspetralliadf:4cgH0uxNSnfOGtr3@pruebahua.olbttjo.mongodb.net/?retryWrites=true&w=majority&appName=pruebaHUA"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client['Hospital']

image = Image.open('Hospital_Austral_Logo_2023.png')
st.image(image, width=100)

st.title("Registro Medico")

st.subheader("Consultar paciente por historia clinica.")
historia_clinica_busqueda = st.text_input("Introduce la historia clinica del paciente", placeholder='123.456')

if st.button('Buscar paciente'):
    if historia_clinica_busqueda:
        try:
            numero_historia_clinica = float(historia_clinica_busqueda)
            paciente_para_mover = db['pacientes'].find_one({"HC": numero_historia_clinica})
            if paciente_para_mover:
                st.write(f"Nombre del paciente: {paciente_para_mover['nombre']} {paciente_para_mover['apellido']}")
            else:
                st.write('No se encuentra ningún paciente con ese número de historia clínica.')
        except ValueError:
            # Capturar el error si no se puede convertir a float
            st.error("Error: Por favor, ingrese un número de historia clínica válido.")
    else:
        st.write('Por favor, ingrese un número de historia clínica para buscar un paciente.')

st.subheader("Seleccione:")

if st.button('Fallecido'):      
    if historia_clinica_busqueda:
        try:
            numero_historia_clinica = float(historia_clinica_busqueda)
            paciente_para_mover = db['pacientes'].find_one({"HC": numero_historia_clinica})

            if paciente_para_mover:
                st.write(f"Nombre del paciente: {paciente_para_mover['nombre']} {paciente_para_mover['apellido']}")
                db['fallecidos'].insert_one(paciente_para_mover)
                db['pacientes'].delete_one({"HC": numero_historia_clinica})
                st.success(f"Registro exitoso.")
            else:
                st.write('No se encuentra ningún paciente con ese número de historia clínica.')
        except ValueError:
            # Capturar el error si no se puede convertir a float
            st.error("Error: Por favor, ingrese un número de historia clínica válido.")
    else:
        st.write('Por favor, ingrese un número de historia clínica para buscar un paciente.')



if st.button('Dar de Alta'):
    if historia_clinica_busqueda:
        try:
            numero_historia_clinica = float(historia_clinica_busqueda)
            paciente_para_mover = db['pacientes'].find_one({"HC": numero_historia_clinica})

            if paciente_para_mover:
                st.write(f"Nombre del paciente: {paciente_para_mover['nombre']} {paciente_para_mover['apellido']}")
                db['alta'].insert_one(paciente_para_mover)
                db['pacientes'].delete_one({"HC": numero_historia_clinica})
                st.success(f"Registro exitoso.")
            else:
                st.write('No se encuentra ningún paciente con ese número de historia clínica.')
        except ValueError:
            # Capturar el error si no se puede convertir a float
            st.error("Error: Por favor, ingrese un número de historia clínica válido.")
    else:
        st.write('Por favor, ingrese un número de historia clínica para buscar un paciente.')

st.divider()

