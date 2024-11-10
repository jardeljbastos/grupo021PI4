import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output
from flask import Flask
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json

server = Flask(__name__)

#app = Dash(__name__, server=server, suppress_callback_exceptions=True)
grupo021PI4 = Dash(__name__, server=server, suppress_callback_exceptions=True)

@server.before_request
def before_first_request():
    pass

df = pd.read_excel("ENEMDados2023.xlsx", engine='openpyxl')

mapa_sexo = {
    'M': 'Masculino',
    'F': 'Feminino'
}

mapa_cor_raca = {
    0: 'Não declarado',
    1: 'Branca',
    2: 'Preta',
    3: 'Parda',
    4: 'Amarela',
    5: 'Indígena',
    6: 'Não dispõe de informação'
}

mapa_estado_civil = {
    0: 'Não informado',
    1: 'Solteiro(a)',
    2: 'Casado(a)/Mora com companheiro(a)',
    3: 'Divorciado(a)/Desquitado(a)/Separado(a)',
    4: 'Viúvo(a)'
}

df['Sexo'] = df['TP_SEXO'].map(mapa_sexo)
df['Cor/Raça'] = df['TP_COR_RACA'].map(mapa_cor_raca)
df['Estado Civil'] = df['TP_ESTADO_CIVIL'].map(mapa_estado_civil)

def create_sex_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]

    df_graph = filtered_df['Sexo'].value_counts().reset_index()
    df_graph.columns = ['Sexo', 'Quantidade']

    fig = px.bar(
        df_graph,
        x='Sexo',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Sexo - ENEM 2023 ({selected_sex})',
        color='Sexo',
        color_discrete_map={'Masculino': '#2E86C1', 'Feminino': '#E74C3C'},
        text='Quantidade'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Sexo",
        yaxis_title="Número de Candidatos",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )

    return fig

def create_race_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]

    df_graph = filtered_df['Cor/Raça'].value_counts().reset_index()
    df_graph.columns = ['Cor/Raça', 'Quantidade']

    total = df_graph['Quantidade'].sum()
    df_graph['Percentual'] = (df_graph['Quantidade'] / total * 100).round(2)

    color_map = {
        'Não declarado': '#808080',
        'Branca': '#E6E6E6',
        'Preta': '#2C3E50',
        'Parda': '#C4A484',
        'Amarela': '#FFD700',
        'Indígena': '#8B4513',
        'Não dispõe de informação': '#D3D3D3'
    }

    fig = px.pie(
        df_graph,
        values='Quantidade',
        names='Cor/Raça',
        title=f'Distribuição de Candidatos por Cor/Raça - ENEM 2023 ({selected_sex})',
        color='Cor/Raça',
        color_discrete_map=color_map,
        hover_data=['Percentual'],
        custom_data=['Quantidade', 'Percentual']
    )

    fig.update_traces(
        textposition='inside',
        textinfo='label+percent',
        hovertemplate="<b>%{label}</b><br>" +
                      "Quantidade: %{customdata[0]:,.0f}<br>" +
                      "Percentual: %{customdata[1]:.2f}%<br>"
    )

    fig.update_layout(
        showlegend=True,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=80, b=120, l=60, r=60)
    )

    return fig

def create_civil_status_graph(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]

    df_graph = filtered_df['Estado Civil'].value_counts().reset_index()
    df_graph.columns = ['Estado Civil', 'Quantidade']

    color_map = {
        'Não informado': '#808080',
        'Solteiro(a)': '#3498DB',
        'Casado(a)/Mora com companheiro(a)': '#2ECC71',
        'Divorciado(a)/Desquitado(a)/Separado(a)': '#E74C3C',
        'Viúvo(a)': '#9B59B6'
    }

    fig = px.bar(
        df_graph,
        x='Estado Civil',
        y='Quantidade',
        title=f'Distribuição de Candidatos por Estado Civil - ENEM 2023 ({selected_sex})',
        color='Estado Civil',
        color_discrete_map=color_map,
        text='Quantidade'
    )

    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title="Estado Civil",
        yaxis_title="Número de Candidatos",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12),
        xaxis={'tickangle': 45}
    )

    return fig


def create_age_histogram(selected_sex='Todos'):
    if selected_sex == 'Todos':
        filtered_df = df
    else:
        filtered_df = df[df['Sexo'] == selected_sex]

    def map_age_group(value):
        if value in [1, 2]:
            return 'Menor de 18 anos'
        elif value in [3, 4, 5, 6]:
            return 'Entre 18 e 21 anos'
        elif value in [7, 8, 9, 10]:
            return 'Entre 22 e 25 anos'
        elif value == 11:
            return 'Entre 26 e 30 anos'
        elif value in [12, 13]:
            return 'Entre 31 e 40 anos'
        elif value in [14, 15]:
            return 'Entre 41 e 50 anos'
        elif value in [16, 17]:
            return 'Entre 51 e 60 anos'
        elif value in [18, 19]:
            return 'Entre 61 e 70 anos'
        elif value == 20:
            return 'Maior de 70 anos'
        return 'Outros'

    filtered_df['Faixa Etária'] = filtered_df['TP_FAIXA_ETARIA'].apply(map_age_group)

    order = ['Menor de 18 anos', 'Entre 18 e 21 anos', 'Entre 22 e 25 anos',
             'Entre 26 e 30 anos', 'Entre 31 e 40 anos', 'Entre 41 e 50 anos',
             'Entre 51 e 60 anos', 'Entre 61 e 70 anos', 'Maior de 70 anos']

    age_counts = filtered_df['Faixa Etária'].value_counts().reset_index()
    age_counts.columns = ['Faixa Etária', 'Quantidade']

    age_counts['Faixa Etária'] = pd.Categorical(
        age_counts['Faixa Etária'],
        categories=order,
        ordered=True
    )
    age_counts = age_counts.sort_values('Faixa Etária')

    fig = px.bar(
        age_counts,
        x='Quantidade',
        y='Faixa Etária',
        orientation='h',
        title=f'Distribuição de Candidatos por Faixa Etária - ENEM 2023 ({selected_sex})',
        color='Faixa Etária',
        color_discrete_map={
            'Menor de 18 anos': '#3498DB',
            'Entre 18 e 21 anos': '#2ECC71',
            'Entre 22 e 25 anos': '#E74C3C',
            'Entre 26 e 30 anos': '#9B59B6',
            'Entre 31 e 40 anos': '#F1C40F',
            'Entre 41 e 50 anos': '#A569BD',
            'Entre 51 e 60 anos': '#5499C7',
            'Entre 61 e 70 anos': '#45B39D',
            'Maior de 70 anos': '#D35400'
        },
        text=age_counts['Quantidade'],
    )

    fig.update_layout(
        xaxis_title="Número de Candidatos",
        yaxis_title="Faixa Etária",
        bargap=0.1,
        bargroupgap=0.1,
        font=dict(size=12),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(l=200, r=50, t=80, b=50)
    )

    return fig


def create_uf_map(data):
    uf_counts = data['SG_UF_PROVA'].value_counts().reset_index()
    uf_counts.columns = ['UF', 'Quantidade']

    geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

    fig = go.Figure()

    fig.add_trace(go.Choroplethmapbox(
        geojson=geojson_url,
        featureidkey='properties.sigla',
        locations=uf_counts['UF'],
        z=uf_counts['Quantidade'],
        colorscale='Reds',
        zmin=uf_counts['Quantidade'].min(),
        zmax=uf_counts['Quantidade'].max(),
        colorbar=dict(
            title=dict(
                text='Quantidade<br>de Candidatos',
                font=dict(size=14)
            ),
            thickness=20,
            len=0.5,
            tickformat=',d'
        ),
        marker=dict(
            opacity=0.7,
            line_width=1
        ),
        hovertemplate='<b>Estado: %{location}</b><br>' +
                      'Candidatos: %{z:,.0f}<extra></extra>'
    ))

    fig.update_layout(
        title=dict(
            text='Distribuição de Candidatos por Estado',
            x=0.5,
            y=0.95,
            font=dict(size=16)
        ),
        mapbox=dict(
            style='carto-positron',
            zoom=2.5,
            center=dict(lat=-15.8, lon=-47.9),
            pitch=0
        ),
        margin=dict(l=0, r=0, t=30, b=0),
        height=600,
        paper_bgcolor='white',
        plot_bgcolor='white'
    )

    fig.update_layout(
        mapbox=dict(
            bearing=0,
            accesstoken='pk.eyJ1IjoibHVjYXNvbGl2ZWlyYWRzIiwiYSI6ImNsc2theHc3dzBndmsya3J0Y2x2Ymh2bzkifQ.V9g9FHCjxM5TguELkDO3pA'
        )
    )

    return fig

grupo021PI4.layout = html.Div(
    children=[
        html.Div(
            className='header',
            children=[
                html.Img(
                    src='/assets/ENEM.png',
                    style={
                        'height': '100px',
                        'marginRight': '20px'
                    }
                ),
                html.H1(
                    children='Análise de Candidatos do ENEM 2023',
                    style={
                        'textAlign': 'center',
                        'color': '#2C3E50',
                        'marginTop': '20px',
                        'marginBottom': '20px',
                        'fontFamily': 'Arial, sans-serif',
                        'flex': '1'
                    }
                ),
                html.Img(
                    src='/assets/Univesp.png',
                    style={
                        'height': '100px',
                        'marginLeft': '20px'
                    }
                ),
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'padding': '20px'
            }
        ),
        html.Div(
            children='''Visualização da distribuição dos candidatos por Sexo, Cor/Raça e Estado Civil no ENEM 2023''',
            style={
                'textAlign': 'center',
                'color': '#7F8C8D',
                'marginBottom': '30px'
            }
        ),

        html.Div(
            children=[
                html.Label(
                    'Selecione o Sexo:',
                    style={
                        'marginRight': '10px',
                        'fontWeight': 'bold',
                        'color': '#2C3E50'
                    }
                ),
                dcc.Dropdown(
                    id='sex-dropdown',
                    options=[
                        {'label': 'Todos', 'value': 'Todos'},
                        {'label': 'Masculino', 'value': 'Masculino'},
                        {'label': 'Feminino', 'value': 'Feminino'}
                    ],
                    value='Todos',
                    style={
                        'width': '200px'
                    }
                )
            ],
            style={
                'display': 'flex',
                'justifyContent': 'center',
                'alignItems': 'center',
                'marginBottom': '20px'
            }
        ),

        html.Div([
            dcc.Graph(
                id='grafico-sexo',
                figure=create_sex_graph(),
                style={'height': '500px'}
            ),
            dcc.Graph(
                id='grafico-raca',
                figure=create_race_graph(),
                style={'height': '500px'}
            ),
            dcc.Graph(
                id='grafico-estado-civil',
                figure=create_civil_status_graph(),
                style={'height': '500px'}
            ),
            dcc.Graph(
                id='grafico-idade',
                figure=create_age_histogram(),
                style={'height': '500px'}
            ),
            dcc.Graph(
                id='uf-map',
                figure=create_uf_map(df[['SG_UF_PROVA']]),
                style={'height': '500px'}
            )
        ])
    ],
    style={
        'padding': '20px',
        'backgroundColor': '#F8F9F9'
    }
)

@callback(
    [Output('grafico-sexo', 'figure'),
     Output('grafico-raca', 'figure'),
     Output('grafico-estado-civil', 'figure'),
     Output('grafico-idade', 'figure'),
     Output('uf-map', 'figure')],
    Input('sex-dropdown', 'value')
)

def update_graphs(selected_sex):
    return create_sex_graph(selected_sex), create_race_graph(selected_sex), create_civil_status_graph(
        selected_sex), create_age_histogram(selected_sex), create_uf_map(df[['SG_UF_PROVA']])

server = grupo021PI4.server

if __name__ == '__main__':
    grupo021PI4.run_server(debug=False, host='0.0.0.0', port=8080)