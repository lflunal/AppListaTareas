# Importa las librerías necesarias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Función para inicializar la aplicación
def inicializar_app():
    if 'tarea_app' not in st.session_state:
        st.session_state.tarea_app = TareaApp()

# Crea una clase para la aplicación
class TareaApp:
    def __init__(self):
        self.tareas = pd.DataFrame(columns=['Descripción', 'Categoría', 'Fecha Límite', 'Estado'])

    def agregar_tarea(self, descripcion, categoria, fecha_limite):
        nueva_tarea = {'Descripción': descripcion, 'Categoría': categoria, 'Fecha Límite': fecha_limite, 'Estado': 'Pendiente'}
        self.tareas = pd.concat([self.tareas, pd.DataFrame([nueva_tarea])], ignore_index=True)

    def actualizar_estado_tarea(self, tarea_idx, nuevo_estado):
        self.tareas.at[tarea_idx, 'Estado'] = nuevo_estado

    def mostrar_tareas(self):
        return self.tareas

    def mostrar_estadisticas(self):
        # Cálculos estadísticos usando numpy
        total_tareas = len(self.tareas)
        tareas_completadas = np.sum(self.tareas['Estado'] == 'Completada')
        tareas_pendientes = total_tareas - tareas_completadas

        # Gráfico de barras usando matplotlib
        categorias = self.tareas['Categoría'].value_counts()
        plt.bar(categorias.index, categorias.values)
        plt.xlabel('Categorías')
        plt.ylabel('Número de Tareas')
        plt.title('Distribución de Tareas por Categoría')
        st.pyplot(plt)

        # Muestra estadísticas
        st.write(f'Total de Tareas: {total_tareas}')
        st.write(f'Tareas Completadas: {tareas_completadas}')
        st.write(f'Tareas Pendientes: {tareas_pendientes}')

# Configura la interfaz de usuario con Streamlit
def main():
    inicializar_app()  # Inicializa la aplicación solo una vez

    st.title('Aplicación de Lista de Tareas')
    st.sidebar.header('Agregar Nueva Tarea')

    # Formulario para agregar nuevas tareas
    descripcion = st.sidebar.text_input('Descripción')
    categoria = st.sidebar.text_input('Categoría')
    fecha_limite = st.sidebar.date_input('Fecha Límite')

    if st.sidebar.button('Agregar Tarea'):
        st.session_state.tarea_app.agregar_tarea(descripcion, categoria, fecha_limite)

    # Muestra las tareas existentes
    st.header('Lista de Tareas')

    tareas_df = st.session_state.tarea_app.mostrar_tareas()

    # Menú desplegable para seleccionar tarea a actualizar
    tarea_seleccionada = st.selectbox('Selecciona una Tarea para Actualizar', tareas_df['Descripción'])

    # Muestra la tarea seleccionada y botones de acción
    if not tareas_df.empty:
        tarea_idx = tareas_df[tareas_df['Descripción'] == tarea_seleccionada].index[0]

        st.write(f"{tarea_seleccionada} - {tareas_df.at[tarea_idx, 'Categoría']} - {tareas_df.at[tarea_idx, 'Fecha Límite']} - Estado: {tareas_df.at[tarea_idx, 'Estado']}")
        
        nuevo_estado = st.radio(f"Actualizar Estado de {tarea_seleccionada}", ('Pendiente', 'Completada'))
        if st.button(f"Actualizar Estado de {tarea_seleccionada}"):
            st.session_state.tarea_app.actualizar_estado_tarea(tarea_idx, nuevo_estado)

    # Muestra estadísticas y gráficos
    st.header('Estadísticas y Gráficos')
    st.session_state.tarea_app.mostrar_estadisticas()

# Ejecuta la aplicación
if __name__ == '__main__':
    main()