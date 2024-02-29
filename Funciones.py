from pymongo import MongoClient
from datetime import datetime
import streamlit as st
import pandas as pd
from PIL import Image

client = MongoClient('localhost', 27017)
db = client['Hospital']

def mostrar_informacion(paciente):     
            if paciente:
                tab1, tab2, tab3, tab4, tab5 = st.tabs([":blue[Informacion paciente]", ":blue[Medicacion / Vias / ATB]",":blue[Cultivos / Laboratorios]", ":blue[Plan de accion / Pendientes]", ":blue[Notas]"])

                with tab1:
                    st.header("Informacion paciente", divider="blue")
                    st.write(f"Apellido: {paciente['apellido']}")
                    st.write(f"Nombre: {paciente['nombre']}")
                    st.write(f"Sector: {paciente['sector']} -  Cama: {paciente['cama']}")
                   # st.write(f"Cama: {paciente['cama']}")
                    st.write(f"Nombre de los padres: {paciente['nombres de los padres']}")
                    st.write(f"Edad: {paciente['edad']}")
                    st.write(f"Peso: {paciente['peso']}")
                    st.write(f"Superficie corporal: {paciente['superficie corporal']}")
                    st.write(f"HC: {paciente['HC']}")
                    st.write(f"Fecha de internacion: {paciente['FI']}")
                    st.write(f"Dieta: {paciente['dieta']}")
                    diagnosticos = paciente.get("diagnóstico", [])
                    st.write(f"Diagnóstico: {', '.join(diagnosticos)}")
                    problemas_activos = paciente.get("problemas activos", [])
                    st.write(f"Problemas activos: {', '.join(problemas_activos)}")

                with tab2:
                    st.header("Medicacion / Vias / ATB", divider="blue")
                    if paciente and "medicacion" in paciente:
                        st.write("Medicación")
                        medicamentos = paciente.get("medicacion", [])
                        datos_medicacion = [{"Medicacion": medicamento['Medicacion'], "Cantidad": medicamento['Cantidad']} for medicamento in medicamentos]
                        st.table(datos_medicacion)
                    else:
                        st.write("No se encontraron medicamentos para este paciente.")

                    if paciente and "Vias" in paciente:
                        st.write("Vias")
                        vias = paciente.get("Vias", [])
                        datos_vias = [{"Vias": via['Vias'], "Fecha de Inicio": via['Fecha'], "D": via['D'], "Fecha de Finalización": via["Fecha de finalización"]} for via in vias]
                        st.table(datos_vias)
                    else:
                        st.write("No se encontraron vias para este paciente.")

                    if paciente and "ATB" in paciente:
                        st.write("ATB")
                        atbs = paciente.get("ATB", [])
                        datos_atb = [{"ATB": atb['ATB'], "Fecha": atb['Fecha'], "D": atb['D'], "Fecha de Finalización": atb["Fecha de finalización"]} for atb in atbs]
                        st.table(datos_atb)
                    else:
                        st.write("No se encontraron antiobioticos para este paciente.")

                with tab3:
                    st.header("Cultivos / Laboratorios", divider="blue")
                    if paciente and "cultivos" in paciente:
                        st.write("Cultivos")
                        cultivos = paciente.get("cultivos", [])
                        datos_cultivos = [{"Fecha": cultivo['Fecha'], "Cultivo": cultivo['Cultivo'], "Resultados": cultivo['Resultado']} for cultivo in cultivos]
                        st.table(datos_cultivos)
                    else:
                        st.write("No se encontraron estudios de cultivos para ese paciente.")
                    if paciente and "laboratorios" in paciente:
                        st.write("Laboratorios")
                        laboratorios = paciente.get("laboratorios", [])
                        datos_laboratorio = [{"Fecha": laboratorio['Fecha'], "Laboratorio": laboratorio['Laboratorio'], "Resultados": laboratorio['Resultado']} for laboratorio in laboratorios]
                        st.table(datos_laboratorio)
                    else:
                        st.write("No se encontraron estudios de laboratorio para ese paciente.")

                with tab4:
                    st.header("Plan de accion / Pendientes", divider='blue')
                    if paciente and "plan_accion / contingencias" in paciente:
                        st.write("Plan de accion / contingencias")
                        plan_acciones = paciente.get("plan_accion / contingencias", [])
                        datos_plan = [{"Fecha": plan_accion['Fecha'], "Medico": plan_accion['Medico'], "Plan de accion": plan_accion['Plan de accion']} for plan_accion in plan_acciones]
                        st.table(datos_plan)
                    else:
                        st.write("No se encontro un plan de accion para ese paciente.")
                    if paciente and "pendientes" in paciente:
                        st.write("Pendientes")
                        pendientes = paciente.get("pendientes", [])
                        datos_pendientes = [{"Fecha": pendiente['Fecha'], "Medico": pendiente['Medico'], "Pendiente": pendiente['Pendiente']} for pendiente in pendientes]
                        st.table(datos_pendientes)
                    else:
                        st.write("No se encontraron pendientes para ese paciente.")

                with tab5:
                    st.header("Notas", divider='blue')
                    if paciente and "notas" in paciente:
                        notas = paciente.get("notas", [])
                        datos_notas = [{"Fecha": nota['Fecha'], "Medico": nota['Medico'], "Notas": nota['Nota']} for nota in notas]
                        st.table(datos_notas)
                    else:
                        st.write("No se encontraron notas para ese paciente.")
            else:
                st.write('No se encontro un paciente con esta historia clinica.')   

def modificar_valor(opcion, campo, historia_clinica_busqueda):
    valor_modificado = st.text_input(opcion)
    if st.button("Modificar Valores", key=f"valores {campo}"):
        if not valor_modificado:
            st.error("Por favor complete la información")
        else:
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$set": {campo: valor_modificado}})
            st.success("Valores agregados con éxito!")


def agregar_informacion(opcion, campo, historia_clinica_busqueda):
    valor_agregado = st.text_input(opcion)
    if st.button("Agregar Valores", key=f"valores {campo}"):
        if not valor_agregado:
            st.error("Por favor complete la información")
        else:
            db['pacientes'].update_one({"HC": float(historia_clinica_busqueda)}, {"$push": {campo: valor_agregado}})
            st.success("Valores agregados con éxito!")
