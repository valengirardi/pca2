import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import plotly.graph_objects as go

# Título de la aplicación
st.title("Gráfico PCA")

# Cargar los datos desde el archivo Excel
file_path = "PCA.xlsx"  # Asegúrate de que el archivo esté presente en el repositorio

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

    # Definir colores específicos para ciertos puntos
    custom_colors = {
        "R3-1": "#ffbf50",
        "R3-2": "#c7519c",
        "R3-3": "#bcbd22",
        "R1": "#1283b2"
    }

    # Crear una lista de colores basada en el tipo de reactor
    colors = [
        custom_colors.get(row['type-of-reactor'], '#cccccc')  # Color por defecto gris si no está en el diccionario
        for _, row in projected_df.iterrows()
    ]

    # Crear un objeto go.Figure
    fig = go.Figure()

    # Añadir los puntos al gráfico
    fig.add_trace(go.Scatter3d(
        x=projected_df['PC1'],
        y=projected_df['PC2'],
        z=projected_df['PC3'],
        mode='markers+text',
        marker=dict(size=5, color=colors, opacity=0.8),
        text=projected_df['type-of-reactor'],
        textposition='top center',
        textfont=dict(size=10, color=colors),  # Aplicar los mismos colores a las etiquetas
        name='Samples'
    ))

    # Lista de variables a filtrar
    variables_to_keep = [
        'pH',
        'Sulfide concentration',
        'Sulfate concentration ',
        'Hydrogen sulfide concentration',
        'Amount of Fe (instantáneo)',
        'S input per day',
        'Methane in biogas (%)',
        'Carbon dioxide in biogas (%)',
        'Uncultured (Family: Anaerolineaceae)',
        'Aminobacterium',
        'Sporanaerobacter',
        'Syntrophomonas',
        'Syner-01',
        'Christensenellaceae_R-7_group',
        'EBM-39',
        'Sphaerochaeta',
        'Proteiniphilum',
        'Thermovirga',
        'Pseudoramibacter',
        'Dethiosulfovibrio',
        'SEEP-SRB1',
        'Desulfobulbus',
        'Desulfobotulus',
        'Desulfomicrobium',
        'Desulfocurvus',
        'Desulfuromonas',
        'Methanobrevibacter',
        'Methanospirillum',
        'Candidatus_Methanoplasma',
        'Methanobacterium',
        'Methanoculleus',
        'Methanocalculus',
        'RumEn_M2',
        'Methanimicrococcus',
    ]

    # Filtrar las variables a mantener
    filtered_columns = [col for col in data.columns if col in variables_to_keep]

    # Escalar la matriz de cargas (loadings) para visualización
    loadings = pca.components_.T  # Cargar la matriz de componentes principales
    scaler = MinMaxScaler(feature_range=(-7.5, 7.5))
    loadings_scaled = scaler.fit_transform(loadings)

    # Diccionario para renombrar las etiquetas (opcional)
    label_mapping = {
        "Amount of Fe (instantáneo)": "Fe³⁺ addition",
        "Sulfide concentration": "H₂Sliq/HS⁻liq",
        "Sulfate concentration ": "SO₄²⁻",
        "Hydrogen sulfide concentration": "H₂Sg",
        "Methane in biogas (%)": "CH₄",
        "Carbon dioxide in biogas (%)": "CO₂",
        "S input per day": "S input"
    }

    # Agregar los vectores de carga (loadings) con leyenda seleccionable y etiquetas
    for i, variable in enumerate(filtered_columns):
        vector = loadings_scaled[data.columns.get_loc(variable), :]  # Obtener el vector escalado

        # Dibujar los vectores como líneas
        fig.add_trace(go.Scatter3d(
            x=[0, vector[0]],
            y=[0, vector[1]],
            z=[0, vector[2]],
            mode='lines',
            line=dict(color='purple', width=1.5),
            name=label_mapping.get(variable, variable),  # Usar el nombre mapeado o el original
            legendgroup=variable,  # Usar el mismo grupo para líneas y texto
            showlegend=True
        ))

        # Dibujar la punta del vector
        fig.add_trace(go.Scatter3d(
            x=[vector[0]],
            y=[vector[1]],
            z=[vector[2]],
            mode='markers',
            marker=dict(size=2, color='purple', symbol='circle', opacity=0.8),
            name=label_mapping.get(variable, variable),  # Usar el nombre mapeado o el original
            legendgroup=variable,  # Usar el mismo grupo para líneas y texto
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
