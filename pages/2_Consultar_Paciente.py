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

st.title("Administrar Paciente") 

st.subheader("Consultar paciente por historia clinica.")
historia_clinica_busqueda = st.text_input("Introduce la historia clinica del paciente", placeholder='123.456')
if st.button('Buscar paciente'):
    if historia_clinica_busqueda:
        try:
            numero_historia_clinica = float(historia_clinica_busqueda)
            paciente = db["pacientes"].find_one({'HC': numero_historia_clinica})
            mostrar_informacion(paciente)

        except ValueError:
            st.error("Error: Por favor, ingrese un número de historia clínica válido.")

st.divider()

option = st.selectbox(
    'Que dato le gustaria editar?',
    ('Nombre', 'Apellido', 'Sector','Nombre de los padres', 'Edad', 'Peso', 'SC', 'HC', 'Diagnostico', 'Problemas activos', 'Medicacion', 'ATB', 'Vias', 'Cultivos', 'Laboratorios', 'Plan de accion / contingencias', 'Pendiente', 'Notas'),
    index=None, placeholder="Seleccione los datos...")

st.write('Usted seleccionó:', option)

if option == 'Nombre':
    modificar_valor("Nombre", "nombre", historia_clinica_busqueda)

elif option == 'Apellido':
    modificar_valor("Apellido", "apellido", historia_clinica_busqueda)

elif option == 'Sector':
    sector = st.selectbox(
    'Seleccione el sector:',
    ('TAMO', 'Abiertas', 'Habitaciones'),
    index=None,
    placeholder="Seleccione el sector...", key = "sector")

    cama = st.text_input("Camilla", placeholder='Agregar el numero de cama', key = 'cama')
    paciente_a_cambiar = db['pacientes'].find_one({"sector": sector, "cama": cama})
    if st.button("Guardar cambio"):
        if not sector or not cama:
            st.error("Por favor complete la información")
        else:
            if paciente_a_cambiar:
                    st.error("Ya hay un paciente asignado a esta cama en el mismo sector. Por favor, elige otra cama.")
            else:
                db["pacientes"].update_many({"HC": float(historia_clinica_busqueda)}, {'$set':{'sector': sector,  "cama": cama}})
                st.success(f"Traslado exitoso.")

elif option == 'Nombre de los padres':
    modificar_valor("Nombre de los padres", "nombres de los padres", historia_clinica_busqueda)

elif option == 'Edad':
    modificar_valor("Edad", "edad", historia_clinica_busqueda)

elif option == 'Peso':
    modificar_valor("Peso", "peso", historia_clinica_busqueda)

elif option == 'SC':
    modificar_valor("Superficie corporal", "superficie corporal", historia_clinica_busqueda)

elif option == 'HC':
    hc = st.text_input("Historia clinica")
    if st.button("Actualizar Valores", key="valores medicacion"):
        try:
            numero_float = float(hc)
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$set": {"HC": float(hc)}})
            st.success("Valores agregados con éxito!")
        except ValueError:
            st.error("Ingrese un número válido en formato 123.456")

elif option == 'Diagnostico':
    agregar_informacion("Diagnóstico", "diagnóstico", historia_clinica_busqueda)

elif option == 'Problemas activos':
    agregar_informacion("Problemas activos", "problemas activos", historia_clinica_busqueda)

elif option == 'Medicacion': 

    # Agregar medicacion nueva
    st.subheader("Agregar medicamento.")
    medicacion = st.text_input("Medicacion")
    cantidad = st.text_input("Cantidad")
    if st.button("Agregar medicación", key="valores medicacion"):
        medicaciones = {"Medicacion": medicacion, "Cantidad": cantidad}
        db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"medicacion": medicaciones}})
        st.success("Valores agregados con éxito!")
    st.divider()

    documento_paciente = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente is not None:
        medicamentos = documento_paciente.get("medicacion", [])
        opciones_medicamentos = [f"{medicamento['Medicacion']} - {medicamento['Cantidad']}" for medicamento in medicamentos]
    else:
        st.error("El paciente no fue encontrado.")

    st.subheader(f"Modificar cantidad del medicamento.") 
    opcion = st.selectbox("Selecciona un medicamento:", opciones_medicamentos, placeholder="Seleccione un medicamento...")
    if opcion is not None:
        nombre_medicamento, cantidad_medicamento = opcion.split(" - ")

    nueva_cantidad = st.text_input("Nueva Cantidad:")
    if st.button("Modificar Medicamento"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "medicacion.Medicacion": nombre_medicamento},
            {"$set": {"medicacion.$.Cantidad": nueva_cantidad}}
        )
        st.success(f"Cantidad de {nombre_medicamento} modificada a: {nueva_cantidad}")

    st.divider()
    
    # Botón para eliminar el medicamento
    documento_paciente_1 = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente_1 is not None:
        medicamentos1 = documento_paciente_1.get("medicacion", [])
        opciones_medicamentos_1 = [f"{medicamento['Medicacion']} - {medicamento['Cantidad']}" for medicamento in medicamentos1]
    else:
        st.error("El paciente no fue encontrado.")
    st.subheader(f"Eliminar medicamento.") 
    opcion1 = st.selectbox("Selecciona un medicamento:", opciones_medicamentos_1, key= 12, placeholder="Seleccione un medicamento...")
    if opcion1 is not None:
        nombre_medicamento1, cantidad_medicamento1 = opcion1.split(" - ")

    if st.button("Eliminar Medicamento"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda)},
            {"$pull": {"medicacion": {"Medicacion": nombre_medicamento1}}}
        )
        st.success(f"{nombre_medicamento1} eliminado con éxito.")

elif option == 'ATB':
    st.subheader('Agregar ATB.')
    ATB = st.text_input("ATB")
    fecha_ATB = st.date_input("Fecha de inicio de antibiotico")
    fecha_final_ATB = st.text_input("Fecha de finalizacion", placeholder= "YYYY-MM-DD")
    
    if st.button("Actualizar valores", key="valores de atb"):

        atb_datetime = datetime.combine(fecha_ATB, datetime.min.time())
        atb_string = atb_datetime.strftime("%Y-%m-%d")
        D_atb = int((datetime.now() - atb_datetime).total_seconds()/ 86400)
        atb = {"ATB": ATB, "Fecha":atb_string, "D": D_atb, "Fecha de finalización": fecha_final_ATB}

        db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"ATB": atb}})
        st.success("Información agregada con éxito!")
    st.divider()
    documento_paciente = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente is not None:
        atbs = documento_paciente.get("ATB", [])
        opciones_atb = [f"{atb['ATB']} - {atb['Fecha']} - {atb['D']} - {atb['Fecha de finalización']}" for atb in atbs]
    # Resto del código para Streamlit
    else:
        st.error("El paciente no fue encontrado.")

# Extraer el nombre del medicamento y la cantidad seleccionada

    st.subheader(f"Modificar ATB.") 
    opcion = st.selectbox("Selecciona un ATB:", opciones_atb, placeholder="Seleccione un ATB...")
    if opcion is not None:
        nombre_atb, fecha_atb, d_atb, fecha_f_atb = opcion.split(" - ")

    nueva_atb = st.text_input("Editar ATB:")
    if st.button("Modificar ATB"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "ATB.ATB": nombre_atb},
            {"$set": {"ATB.$.ATB": nueva_atb}}
        )
        st.success(f"{nombre_atb} modificada a: {nueva_atb}")

    st.divider()
    documento_paciente1 = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente1 is not None:
        atbs1 = documento_paciente1.get("ATB", [])
        opciones_atb1 = [f"{atb['ATB']} - {atb['Fecha']} - {atb['D']} - {atb['Fecha de finalización']}" for atb in atbs1]
    # Resto del código para Streamlit
    else:
        st.error("El paciente no fue encontrado.") 

    st.subheader(f"Modificar fecha de finalización del ATB.") 
    opcion1 = st.selectbox("Selecciona un ATB:", opciones_atb1, key = 14, placeholder="Seleccione un ATB...")
    if opcion1 is not None:
        nombre_atb1, fecha_atb1, d_atb1, fecha_f_atb1 = opcion1.split(" - ")

    nuevo_atb1 = st.text_input("Editar fecha de ATB:", placeholder= 'YYYY-MM-DD')
    if st.button("Modificar fecha de ATB"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "ATB.ATB": nombre_atb},
            {"$set": {"ATB.$.Fecha de finalización": nuevo_atb1}}
        )
        st.success(f"La fecha de {nombre_atb} fue modificada a: {nuevo_atb1}")

elif option == 'Vias':
    st.subheader('Agregar vía.')
    Vias = st.text_input("Vias")
    fecha_vias = st.date_input("Fecha de inicio de la via")
    fecha_final_vias = st.text_input("Fecha de finalizacion", placeholder= "YYYY-MM-DD")

    if st.button("Actualizar valores", key="valores de vias"):

        vias_datetime = datetime.combine(fecha_vias, datetime.min.time())
        vias_string = vias_datetime.strftime("%Y-%m-%d")
        D_vias = int((datetime.now() - vias_datetime).total_seconds()/86400)
        vias = {"Vias": Vias, "Fecha":vias_string, "D": D_vias, "Fecha de finalización": fecha_final_vias}

        db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"Vias": vias}})
        st.success("Información agregada con éxito!")

    documento_paciente = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente is not None:
        vias = documento_paciente.get("Vias", [])
        opciones_vias = [f"{via['Vias']} - {via['Fecha']} - {via['D']} - {via['Fecha de finalización']}" for via in vias]
    else:
        st.error("El paciente no fue encontrado.")

    st.divider()

    st.subheader(f"Modificar Vías.") 
    opcion = st.selectbox("Selecciona una Vía:", opciones_vias, placeholder="Seleccione un Vía...")
    if opcion is not None:  
        nombre_via, fecha_via, d_via, fecha_f_via = opcion.split(" - ")

    nueva_via = st.text_input("Editar Vía:")
    if st.button("Modificar Vía"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "Vias.Vias": nombre_via},
            {"$set": {"Vias.$.Vias": nueva_via}}
        )
        st.success(f"{nombre_via} modificada a: {nueva_via}")
    st.divider()
    documento_paciente1 = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente1 is not None:
        vias1 = documento_paciente1.get("Vias", [])
        opciones_via1 = [f"{via1['Vias']} - {via1['Fecha']} - {via1['D']} - {via1['Fecha de finalización']}" for via1 in vias1]
    else:
        st.error("El paciente no fue encontrado.") 

    st.subheader(f"Modificar fecha de finalización de la via.") 
    opcion1 = st.selectbox("Selecciona una via:", opciones_via1, key = 14, placeholder="Seleccione una via...")
    if opcion1 is not None:
        nombre_via1, fecha_via1, d_via1, fecha_f_via1 = opcion1.split(" - ")

    nuevo_via1 = st.text_input("Editar fecha de la Vía:" , placeholder= 'YYYY-MM-DD')
    if st.button("Modificar fecha de via"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "Vias.Vias": nombre_via},
            {"$set": {"Vias.$.Fecha de finalización": nuevo_via1}}
        )
        st.success(f"La fecha de {nombre_via} fue modificada a: {nuevo_via1}")

elif option == 'Plan de accion / contingencias':
    fecha_plan_accion_datetime = datetime.now()
    plan_accion_texto = st.text_area("Plan de accion / contingencias")
    medico = st.text_input("Médico")

    if st.button("Agregar valores", key="valores plan de accion"):
        if not plan_accion_texto or not medico:
            st.error("Por favor complete la información")
        else:
            plan = {"Fecha": fecha_plan_accion_datetime, "Medico": medico, "Plan de accion": plan_accion_texto}
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"plan_accion / contingencias": plan}})
            st.success("Informacion agregada con éxito!")

elif option == 'Pendiente':
    fecha_pendientes_datetime = datetime.now()
    pendientes_texto = st.text_area("Pendientes")
    medico = st.text_input("Médico")

    if st.button("Agregar Valores", key="valores penditnes"):
        if not pendientes_texto or not medico:
            st.error("Por favor complete la información")
        else:
            pendientes = {"Fecha": fecha_pendientes_datetime, "Medico": medico, "Pendiente": pendientes_texto}
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"pendientes": pendientes}})
            st.success("Informacion agregada con éxito!")

elif option == "Notas":
    fecha_nota_datetime = datetime.now()
    nota_texto = st.text_area("Notas")
    medico = st.text_input("Médico")
    if st.button("Agregar Valores", key="valores notas"):
        if not nota_texto or not medico:
            st.error("Por favor complete la información")
        else: 
            nota = {"Fecha": fecha_nota_datetime, "Medico": medico, "Nota": nota_texto}
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"notas": nota}})
            st.success("Valores agregados con éxito!")

elif option == "Cultivos":
    st.subheader('Agregar cultivo.')
    fecha_cultivos_datetime = st.date_input("Ingrese fecha")
    cultivos_texto = st.text_input("Cultivos")
    resultado_texto = st.text_input("Resultado")

    if st.button("Actualizar Valores", key="valores cultivos"):

        cultivos_datetime = datetime.combine(fecha_cultivos_datetime, datetime.min.time())
        cultivos_str = cultivos_datetime.strftime("%Y-%m-%d")

        nota = {"Fecha": cultivos_str, "Cultivo": cultivos_texto, "Resultado": resultado_texto}
        db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"cultivos": nota}})
        st.success("Valores agregados con éxito!")
    st.divider()
    documento_paciente = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente is not None:
        cultivos = documento_paciente.get("cultivos", [])
        opciones_cultivos = [f"{cultivo['Fecha']} - {cultivo['Cultivo']} - {cultivo['Resultado']}" for cultivo in cultivos]
    else:
        st.error("El paciente no fue encontrado.")

# Extraer el nombre del cultivo y la cantidad seleccionada


    st.subheader(f"Modificar la información de cultivo.") 
    opcion = st.selectbox("Selecciona un cultivo:", opciones_cultivos, placeholder="Seleccione un cultivo...")
    if opcion is not None:
        fecha_cultivo, nombre_cultivo, resultado_cultivo = opcion.split(" - ")

    nuevo_cultivo = st.text_input("Editar cultivo:")
    if st.button("Modificar Cultivo"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "cultivos.Cultivo": nombre_cultivo},
            {"$set": {"cultivos.$.Cultivo": nuevo_cultivo}}
        )
        st.success(f"{nombre_cultivo} modificado a: {nuevo_cultivo}")
    st.divider()

    st.subheader("Modificar el resultado de cultivo.")

    documento_paciente1 = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente1 is not None:
        cultivos1 = documento_paciente1.get("cultivos", [])
        opciones_cultivos1 = [f"{cultivo['Fecha']} - {cultivo['Cultivo']} - {cultivo['Resultado']}" for cultivo in cultivos1]
    else:
        st.error("El paciente no fue encontrado.") 

    opcion1 = st.selectbox("Selecciona un cultivo:", opciones_cultivos1, key = 9, placeholder="Seleccione un cultivo...")
    if opcion1 is not None:
        fecha_cultivo1, nombre_cultivo1, resultado_cultivo1 = opcion.split(" - ")  

    nuevo_resultado1 = st.text_input('Editar resultado:')
    if st.button("Modificar Resultado"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "cultivos.Cultivo": nombre_cultivo1},
            {"$set": {"cultivos.$.Resultado": nuevo_resultado1}}
        )
        st.success(f"El resultado de {nombre_cultivo1} fue modificado a: {nuevo_resultado1}")      

elif option == "Laboratorios":

    st.subheader('Agregar laboratorio.')
    fecha_lab_datetime = st.date_input("Ingrese fecha")
    lab_texto = st.text_area("Laboratorio")
    resultado_texto = st.text_input("Resultado")

    if st.button("Actualizar Valores", key="valores labs"):

        lab_datetime = datetime.combine(fecha_lab_datetime, datetime.min.time())
        lab_str = lab_datetime.strftime("%Y-%m-%d")

        nota = {"Fecha": lab_str, "Laboratorio": lab_texto, "Resultado": resultado_texto}
        db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {"laboratorios": nota}})
        st.success("Valores agregados con éxito!")
    st.divider()
    documento_paciente = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente is not None:
        laboratorios = documento_paciente.get("laboratorios", [])
        opciones_laboratorio = [f"{laboratorio['Fecha']} - {laboratorio['Laboratorio']} - {laboratorio['Resultado']}" for laboratorio in laboratorios]
    else:
        st.error("El paciente no fue encontrado.")

# Extraer el nombre del cultivo y la cantidad seleccionada

    st.subheader(f"Modificar la información del laboratorio.") 
    opcion = st.selectbox("Seleccione un laboratorio:", opciones_laboratorio, placeholder="Seleccione un laboratorio...")
    if opcion is not None:
        fecha_lab, nombre_lab, resultado_lab = opcion.split(" - ")

    nuevo_lab = st.text_input("Editar laboratorio:")
    if st.button("Modificar Laboratorio"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "laboratorios.Laboratorio": nombre_lab},
            {"$set": {"laboratorios.$.Laboratorio": nuevo_lab}}
        )
        st.success(f"{nombre_lab} modificado a: {nuevo_lab}")
    st.divider()
    documento_paciente1 = db["pacientes"].find_one({"HC": float(historia_clinica_busqueda)})

    if documento_paciente1 is not None:
        laboratorios1 = documento_paciente1.get("laboratorios", [])
        opciones_lab1 = [f"{laboratorio['Fecha']} - {laboratorio['Laboratorio']} - {laboratorio['Resultado']}" for laboratorio in laboratorios1]
    else:
        st.error("El paciente no fue encontrado.") 

    opcion1 = st.selectbox("Selecciona un laboratorio:", opciones_lab1, key = 9, placeholder="Seleccione un laboratorio...")
    if opcion1 is not None:
        fecha_lab1, nombre_lab1, resultado_lab1 = opcion.split(" - ")  

    nuevo_resultado1 = st.text_input("Editar resultado del laboratorio:")
    if st.button("Modificar Resultado"):
        db["pacientes"].update_one(
            {"HC": float(historia_clinica_busqueda), "laboratorios.Laboratorio": nombre_lab1},
            {"$set": {"laboratorios.$.Resultado": nuevo_resultado1}}
        )
        st.success(f"El resultado de {nombre_lab1} fue modificado a: {nuevo_resultado1}")      









