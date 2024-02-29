import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from PIL import Image

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


uri = "mongodb+srv://lucaspetralliadf:4cgH0uxNSnfOGtr3@pruebahua.olbttjo.mongodb.net/?retryWrites=true&w=majority&appName=pruebaHUA"

# Create a new client and connect to the server
client = MongoClient(uri, tls=True, server_api=ServerApi('1'))
db = client['Hospital']
    
image = Image.open('Hospital_Austral_Logo_2023.png')
st.image(image, width=100)

# Título de la aplicación
st.title("Nuevo Paciente")

# Para agregar un paciente
st.subheader("Agregar nuevo paciente")
nombre = st.text_input("Nombre", placeholder='Agregar nombre')
apellido = st.text_input("Apellido", placeholder='Agregar apellido')

sector = st.selectbox(
    'Seleccione el sector:',
    ('TAMO', 'Abiertas', 'Habitaciones'),
    index=None,
    placeholder="Seleccione el sector...")

cama = st.text_input("Camilla", placeholder='Agregar el numero de cama')

padres = st.text_input("Nombre de los padres", placeholder='Agregar nombre de los padres')
E = st.text_input("Edad", placeholder='Agregar edad')
P = st.text_input("Peso", placeholder='Agregar peso')
SC = st.text_input("Superficie corporal", placeholder='Superficie corporal')
HC = st.text_input("HC", placeholder='Agregar historia clinica')

FI = st.date_input("Fecha de internacion")
st.write('La fecha de internacion fue:', FI)

DG = st.text_area("Diagnostico",  placeholder='Agregar diagnostico')

problemas_activos = st.text_area("Problemas activos", placeholder='Agregar problemas activos')

dieta = st.text_input("Dieta", placeholder='Agregar dieta')

def crear_documento_paciente(nombre, apellido, sector, cama, padres, E, P, SC, HC, FI, DG, problemas_activos, dieta):
    FI_datetime = datetime.combine(FI, datetime.min.time())
    FI_string = FI_datetime.strftime("%Y-%m-%d")

    # Comprobar si tanto DG como problemas_activos están vacíos
    if not DG and not problemas_activos:
        diagnóstico = []
        problemas = []
    else:
        diagnóstico = [DG] if DG else []
        problemas = [problemas_activos] if problemas_activos else []

    paciente = {
        "nombre": nombre,
        "apellido": apellido,
        "sector": sector,
        "cama": cama,
        "nombres de los padres": padres,
        "edad": E,
        "peso": P,
        "superficie corporal": SC,
        "HC": float(HC),
        "FI": FI_string,
        "diagnóstico": diagnóstico,
        "problemas activos": problemas,
        "dieta": dieta,
    }
    return paciente

if st.button("Agregar Paciente"):
    if not nombre or not apellido or not sector or not E or not P or not SC or not HC:
        st.error("Por favor complete la información")
    else:
        paciente_existente = db['pacientes'].find_one({"sector": sector, "cama": cama})
        if paciente_existente:
            st.error("Ya hay un paciente asignado a esta cama en el mismo sector. Por favor, elige otra cama.")
        else:
            paciente = crear_documento_paciente(nombre, apellido, sector, cama, padres, E, P, SC, HC, FI, DG, problemas_activos, dieta)
            db['pacientes'].insert_one(paciente)
            st.success("Paciente agregado con éxito!")

st.divider()

st.subheader("Reingresar paciente dado de alta")

historia_clinica_busqueda = st.text_input("Introduce la historia clinica del paciente", placeholder='123.456')
sector = st.selectbox(
    'Seleccione el sector:',
    ('TAMO', 'Abiertas', 'Habitaciones'),
    index=None,
    placeholder="Seleccione el sector...", key = "sector")

cama = st.text_input("Camilla", placeholder='Agregar el numero de cama', key = 'cama')



if st.button("Reingresar paciente"):
    if historia_clinica_busqueda:
        try:
            numero_historia_clinica = float(historia_clinica_busqueda)
            paciente_para_mover = db['alta'].find_one({"HC": numero_historia_clinica})
            paciente_existente = db['pacientes'].find_one({"sector": sector, "cama": cama})
            if paciente_existente:
                st.error("Ya hay un paciente asignado a esta cama en el mismo sector. Por favor, elige otra cama.")
            else: 
                if paciente_para_mover:
                    db['pacientes'].insert_one(paciente_para_mover)
                    db["pacientes"].update_many({"HC": numero_historia_clinica}, {'$set':{'sector': sector,  "cama": cama}})
                    db['alta'].delete_one({"HC": numero_historia_clinica})
                    st.write(f"El paciente {paciente_para_mover['nombre']} {paciente_para_mover['apellido']} ha sido reingresado.")
                    st.success(f"Registro exitoso.")
                else:
                    st.write('No se encuentra ningún paciente con ese número de historia clínica.')
        except ValueError:
            # Capturar el error si no se puede convertir a float
            st.error("Error: Por favor, ingrese un número de historia clínica válido.")
    else:
        st.write('Por favor, ingrese un número de historia clínica para reingresar un paciente.')

