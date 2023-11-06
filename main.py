from flask import Flask
import dash
from dash import html, dcc
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

# Cria uma nova aplicação Flask 
server = Flask(__name__)

# Cria uma nova aplicação Dash e usa o servidor Flask como o servidor por trás do Dash
app = dash.Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dados para os gráficos
dados = [
    {'nome': 'CARGA / ENTRADA', 'valor': 44.6, 'var': 4.2},
    {'nome': 'PRODUÇÃO', 'valor': 152.3, 'var': 12.1},
    {'nome': 'TEMPOS PROCESSAMENTO', 'valor': 152.3, 'var': 12.1},
    {'nome': 'VARIABILIDADE', 'valor': 152.3, 'var': 12.1},
    {'nome': 'CONFIABILIDADE', 'valor': 152.3, 'var': 12.1},
    {'nome': 'PARÂMETROS DE OPERAÇÃO', 'valor': 152.3, 'var': 12.1},
    {'nome': 'ESTOQUE', 'valor': 152.3, 'var': 12.1},
    {'nome': 'ENTREGA - SAÍDA', 'valor': 152.3, 'var': 12.1},
    {'nome': 'PONTO ÓTIMO', 'valor': 152.3, 'var': 12.1},
]

# Função para gerar gráfico de indicador (medidor)
def generate_gauge_chart(name, value, var):
    text_color = 'rgb(15, 47, 89)'  # Example text color
    text_size = 16  # Example text size

    # Set the background color for the gauge chart here
    gauge_bg_color = 'rgb(244,244,244)'  # Example background color

    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': name, 'font': {'size': text_size, 'color': text_color}},
        delta={'reference': var, 'increasing': {'color': text_color}},
        gauge={
            'axis': {
                'range': [None, 100],
                'tickwidth': 1,
                'tickcolor': 'white',  # Corrected property to set tick mark color
            },
            'bar': {'color': 'darkblue'},
            'bgcolor': gauge_bg_color,  # Set the gauge background color here
        }
    ))

    fig.update_layout(
        autosize=False,
        width=250,
        height=200,
        margin=dict(l=10, r=10, b=10, t=30),
        paper_bgcolor='rgb(244,244,244)',  # Set the plot background color (transparent here)
        font={'color': text_color, 'size': text_size}
    )

    return fig

# Função para criar medidor com botões
def create_gauge_with_buttons(name, value, var):
    gauge_chart = dcc.Graph(
        figure=generate_gauge_chart(name, value, var),
        style={'height': '200px', 'width': '100%'},  # Use 100% width to fill the column
        className='mx-auto d-block'  # This class centers the gauge
    )

    buttons = html.Div([
        dbc.Button("Tendência", style={
            'width': '50%',
            'backgroundColor': 'rgb(128, 128, 128)',
            'color': 'rgb(255, 255, 255)',
            'borderColor': 'rgb(128, 128, 128)'
        }, className="me-1"),
        dbc.Button("Analytics", style={
            'width': '50%',
            'backgroundColor': 'rgb(128, 128, 128)',
            'color': 'rgb(255, 255, 255)',
            'borderColor': 'rgb(128, 128, 128)'
        }),
    ], className="d-flex", )

    return html.Div([
        gauge_chart,
        buttons
    ], style={
        'border': '2px solid #CCCCCC',
        'borderRadius': '10px',
        'padding': '10px',
        'margin': '5px',  # Reduced margin
        'boxShadow': '0px 0px 10px rgba(0,0,0,0.1)'
    })

# Layout do aplicativo Dash
app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.H1('INSIGHTS | Aparelho de destilação',
                                style={'textAlign': 'left', 'color': 'rgb(15, 47, 89)'}),
                        width=8,
                        style={ 'alignItems': 'left'}),  # Garante alinhamento vertical do título
                dbc.Col(html.Img(src='/assets/logo.png', height='75px'),
                        width=4,
                        style={'textAlign': 'right'}),
                # Garante alinhamento vertical do logotipo
            ],

        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H2('Aparelho de Destilação', style={'color': 'white'}),
                        ],
                        style={'backgroundColor': 'rgb(128, 128, 128)', 'padding': '10px', 'borderRadius': '10px', 'width': '100%','textAlign': 'center'}
                    ),
                    width=10,
                    style={'alignItems': 'center', 'display': 'flex'},
                ),
                dbc.Col(
                    [
                        dbc.Button("-", outline=True, color="secondary", className="me-1",style={'height': '65px', 'width': '65px'}),
                        dbc.Button("o", outline=True, color="secondary", className="me-1",style={'height': '65px', 'width': '65px'}),
                        dbc.Button("x", outline=True, color="secondary", className="me-1",style={'height': '65px', 'width': '65px'}),
                    ],
                    width=2,
                    style={
                        'display': 'flex',
                        'alignItems': 'center',  # Alinha os botões verticalmente no centro
                        'justifyContent': 'center',  # Centraliza os botões horizontalmente
                        'height': '100%'  # Define a altura da coluna para 100% para permitir o alinhamento vertical
                    },
                )
            ],
            align='center',  # Alinha verticalmente
            justify='between',  # Espaçamento entre colunas
        ),

        dbc.Container(
            [
                dbc.Row([
                    # Ensure justify is set to 'center' to center the columns
                    dbc.Col(create_gauge_with_buttons(dado['nome'], dado['valor'], dado['var']), md=2)
                    for dado in dados[:3]
                ]),  # Center the columns in the row
                dbc.Row([
                    dbc.Col(create_gauge_with_buttons(dado['nome'], dado['valor'], dado['var']), md=2)
                    for dado in dados[3:6]
                ],),
                dbc.Row([
                    dbc.Col(create_gauge_with_buttons(dado['nome'], dado['valor'], dado['var']), md=2)
                    for dado in dados[6:9]
                ], style={'align': 'center'}),  # Reduced top margin
            ],
            fluid=True,
        )
    ],
    style={'padding': '50px', 'backgroundColor': 'rgb(244,244,244)', 'minHeight': '100vh'}  # Altura mínima de 100vh
)

# Defina a rota principal do Flask para servir o aplicativo Dash
@server.route("/")
def my_dash_app():
    return app.index()

# Condição para rodar o app
if __name__ == '__main__':
    app.run_server(debug=True)
