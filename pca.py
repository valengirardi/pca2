# Colores para los puntos
color_map = {
    'type1': '#ffbf50',
    'type2': '#c7519c',
    'type3': '#bcbd22',
    'type4': '#1283b2'
}

# Asegúrate de que 'type-of-reactor' tenga valores que correspondan a las claves de `color_map`
projected_df['color'] = projected_df['type-of-reactor'].map(color_map)

# Añadir los puntos al gráfico
for reactor_type, color in color_map.items():
    subset = projected_df[projected_df['type-of-reactor'] == reactor_type]
    fig.add_trace(go.Scatter3d(
        x=subset['PC1'],
        y=subset['PC2'],
        z=subset['PC3'],
        mode='markers+text',
        marker=dict(size=5, color=color, opacity=0.8),
        text=subset['type-of-reactor'],
        textposition='top center',
        textfont=dict(size=10, color='white', family='Arial', bold=True),
        name=reactor_type
    ))

