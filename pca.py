import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go

# Título de la aplicación
st.title("Gráfico PCA")

# Cargar los datos desde el archivo Excel
file_path = "PCA.xlsx"

try:
    # Leer el archivo Excel
    data = pd.read_excel(file_path)

    # Establecer 'sample-id' como el índice del DataFrame
    data.set_index('sample-id', inplace=True)

    # Escalar los datos numéricos
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    # Aplicar PCA para reducir a 3 componentes principales
    pca = PCA(n_components=3)
    projected_data = pca.fit_transform(scaled_data)

    # Convertir los datos proyectados a un DataFrame
    projected_df = pd.DataFrame(data=projected_data, columns=[f'PC{i}' for i in range(1, 4)])
    projected_df['type-of-reactor'] = data.index

    # Normalizar valores de 'type-of-reactor'
    projected_df['type-of-reactor'] = projected_df['type-of-reactor'].str.strip().str.lower()

    # Diccionario de colores ajustado según los valores en tu archivo
    color_map = {
        'r1': '#ffbf50',
        'r3-1': '#c7519c',
        'r3-2': '#bcbd22',
        'r3-3': '#1283b2'
    }

    # Mapear colores
    projected_df['color'] = projected_df['type-of-reactor'].map(color_map)

    # Revisar registros con color faltante
    missing_colors = projected_df[projected_df['color'].isna()]
    if not missing_colors.empty:
        st.error("Hay registros con tipos de reactor no mapeados. Por favor revisa:")
        st.write(missing_colors)

    # Crear un objeto go.Figure
    fig = go.Figure()

    # Añadir los puntos al gráfico con etiquetas (cartelitos)
    for reactor_type, color in color_map.items():
        subset = projected_df[projected_df['type-of-reactor'] == reactor_type]
        fig.add_trace(go.Scatter3d(
            x=subset['PC1'],
            y=subset['PC2'],
            z=subset['PC3'],
            mode='markers+text',
            marker=dict(size=5, color=color, opacity=0.8),
            text=subset['type-of-reactor'],  # Cartelitos con el valor del punto
            textposition='top center',
            textfont=dict(size=10, color='white', family='Arial Black'),
            name=reactor_type
        ))

    # Escalar la matriz de cargas (loadings) para visualización
    loadings = pca.components_.T  # Matriz de componentes principales
    scaler = MinMaxScaler(feature_range=(-7.5, 7.5))
    loadings_scaled = scaler.fit_transform(loadings)

    # Lista de variables a mostrar en los vectores
    variables_to_keep = [
        'pH',
        'Sulfide concentration',
        'Sulfate concentration ',
        'Hydrogen sulfide concentration',
        'Amount of Fe (instantáneo)',
        'S input per day',
        'Methane in biogas (%)',
        'Carbon dioxide in biogas (%)',
        'Biogas volume',
    ]

    # Diccionario opcional para renombrar etiquetas
    label_mapping = {
        "Amount of Fe (instantáneo)": "Iron added",
        "Sulfide concentration": "S²⁻ concentration",
        "Sulfate concentration ": "SO₄²⁻ concentration",
        "Hydrogen sulfide concentration": "H₂S concentration",
        "Methane in biogas (%)": "CH₄ in biogas",
        "Carbon dioxide in biogas (%)": "CO₂ in biogas",
        "S input per day": "S input"
    }

    # Agregar vectores de carga (loadings) con etiquetas
    for i, variable in enumerate(data.columns):
        if variable in variables_to_keep:
            vector = loadings_scaled[i, :]  # Obtener el vector escalado
            fig.add_trace(go.Scatter3d(
                x=[0, vector[0]],
                y=[0, vector[1]],
                z=[0, vector[2]],
                mode='lines+text',
                line=dict(color='purple', width=1.5),
                text=[None, label_mapping.get(variable, variable)],  # Etiqueta al final del vector
                textposition='top center',
                textfont=dict(size=8, color='purple'),
                name=label_mapping.get(variable, variable),
                showlegend=False
            ))

    # Personalizar las etiquetas de los ejes con la varianza explicada
    fig.update_layout(scene=dict(
        xaxis_title=f'PC1 ({pca.explained_variance_ratio_[0]:.2%})',
        yaxis_title=f'PC2 ({pca.explained_variance_ratio_[1]:.2%})',
        zaxis_title=f'PC3 ({pca.explained_variance_ratio_[2]:.2%})'
    ))

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

except FileNotFoundError:
    st.error(f"El archivo '{file_path}' no se encontró. Por favor, súbelo al repositorio.")





