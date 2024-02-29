import streamlit as st
from pymongo import MongoClient
from datetime import datetime
from PIL import Image


# # Configuración de la conexión a MongoDB
# client = MongoClient('localhost', 27017) 
# db = client['hospital']  


image = Image.open('Hospital_Austral_Logo_2023.png')
st.image(image, use_column_width=True)

# Título centralizado
css = """
<style>
h1, h2 {
    text-align: center;
}
</style>
"""
st.markdown(css, unsafe_allow_html=True)
st.title(":gray[Unidad de Cuidados Intensivos Pediatricos]")

