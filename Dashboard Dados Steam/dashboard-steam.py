from multiprocessing.sharedctypes import Value
import pandas as pd
import plotly as py
import plotly.offline as po
import plotly.graph_objs as go
import plotly.express as px
from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, ClientsideFunction
import dash_bootstrap_components as dbc
import numpy as np
from dash_html_components import Div,H1,P,H3
from dash_core_components import Graph, Slider, Checklist



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

#================= Gráfico avaliação dos jogos ===============================
base_metacritic = pd.read_csv('all_games.csv')  #importando base de dados

matriz = base_metacritic.values.tolist()  #transformação matricial

#Filtrado informações apenas dos jogos da plataforma steam

steam_games =[]

for lista in matriz:
    if lista[1] == ' PC':
        steam_games.append(lista)

todos_jogos = [] #criar lista com todos os jogos para a seleção no dropdown

#Função para criar o GRÁFICO
def criargrafico(namejogo):
    #Filtrando dados que serão utilizados
    jogo = []
    metascore = []
    user_review = []

    for c in range (len(steam_games)):
        todos_jogos.append(steam_games[c][0]) #add na lista p dropdown
        if steam_games[c][0] in namejogo:
            jogo.append(steam_games[c][0]) 
            metascore.append(steam_games[c][4]) 
            user_review.append(steam_games[c][5]) 

    #filtro para remover todas as strings iguais a'tbd' da lista de notas dos usuarios

    user_review = list(filter(('tbd').__ne__, user_review)) #O __ne__ significa não igual, substitui o sinal "!="

    #Tornar as strings em valores float

    float_lst = []

    for valor in user_review:
        float_lst.append(float(valor))

    #Transformar as notas dos usuários para uma escala de 0 a 100

    review = list(map(lambda x: x*10, float_lst)) #uma função para multiplicar cada valor da lista por 10

    fig = go.Figure(layout={"template":"plotly_dark"}) 

    fig.add_trace(go.Bar(x = namejogo, y = metascore, name = "Avaliação dos jogadores",marker = {'color' : '#40E0D0'}))
    fig.add_trace(go.Bar(x = namejogo, y = review, name = "Avaliação da critica",marker = {'color' : '#FF1493'}))
    return fig


jogos = ['Half-Life 2'] #1° jogo a ser apresentado no grafico

#============== GRÁFICO JOGADORES PANDEMIA =================================
db = pd.read_csv('Valve_Player_Data.csv')
data = db.values.tolist() #transformação matricial

#estrutura de repetição para listar todos os nomes dos jogos
nome = []
for c in range (len(data)):
  nome.append(data[c][7])

#função para gerar o gráfico
def dado_jogo(jojin):
  tempo = []
  listano = []
  jogadores = []
  jogadores_totais = []
  tempo_total = []
  tempo = []
  
  total = nome.count(jojin)#contar quantas vezes o nome do jogo aparece
  local = nome.index(jojin)#mostra onde a primeira menção do jogo
  
  todo = total + local

  #estrutura de repetição para pegar todas as informações de determindo jogo
  for j in range (local, todo):
    mes, ano = data[j][0].split()#separando mes do ano
    ano = int(ano)
    listano.append(ano)
    jogadores_totais.append(data[j][1])
    tempo_total.append(data[j][0])

  #determina em quais anos as informações vão aparecer
  if len(listano) >= 25:
    inicio = listano.index(2020)#data antes de 2020
    fim = listano.index(2018)#data depois de 2018
  else: #Jogos depois de 2019
    inicio = 0
    fim = len(listano)

  #restringindo as informaçõs para aquela determinada data
  for d in range (inicio, fim):
    jogadores.append(jogadores_totais[d]) 
    tempo.append(tempo_total[d])

  #invertendo a ordem da lista(decrescente para crescente)
  tempo = tempo[::-1]#inversão de lista
  jogadores = jogadores[::-1]

  #parametros do grafico 
  fig = px.line(x= tempo, y= jogadores, title = jojin, height = 400, width = 1000,template = 'plotly_dark')
  fig.update_traces(line_color='#D2691E', line_width=5)
  fig.update_xaxes(title = 'tempo' )
  fig.update_yaxes(title = 'Jogadores' )
  return fig

nome_filtrado = []
[nome_filtrado.append(x) for x in nome if x not in nome_filtrado]

# ================GRÁFICO QUANTIDADE JOGADORES TOTAIS MÊS======================
db = pd.read_csv('Valve_Player_Data.csv')
data = db.values.tolist() #transformação matricial

#estrutura de repetição para listar todos os nomes dos jogos
so_ano = []

for j in range(len(data)):
    mes, ano = data[j][0].split()#separando mes do ano
    ano = int(ano)
    so_ano.append(ano)
so_ano.sort(key=int)

def por_ano(ano): #definição de filtragem do gráfico por ano
  anos = [] # criando lista
  jogos = []

  for c in range(len(data)): #definindo a leitura da base de dados 
    deck = data[c][6] #pegando a primeira coluna da database
    if ano == deck[0:4]: #uma forma de identificar o ano, pois as quatros primeiros caracteres são referentes ao ano
      anos.append(data[c][0]) #pegando as informações referentes aquele específico ano
      jogos.append(data[c][1])
    else:
      pass

  fig = px.area(x= anos, y = jogos, height = 800, width = 1200,template = 'plotly_dark') #definindo modelo do gráfico, eixos e dimensões
  fig.update_yaxes(title= 'Quantidade de Jogadores em milhões') #definindo titulo dos eixos 
  fig.update_xaxes(title= "Anos") #definindo titulo dos eixos
  return fig

def todos(a):
    anos = []
    jogos = []
    for c in range(len(data)):
        anos.append(data[c][0])
        jogos.append(data[c][1])
    fig = px.area(x= anos, y = jogos, height = 800, width = 1200,template = 'plotly_dark') #definindo modelo do gráfico, eixos e dimensões
    fig.update_yaxes(title= 'Quantidade de Jogadores em milhões') #definindo titulo dos eixos 
    fig.update_xaxes(title= "Anos") #definindo titulo dos eixos
    fig.update_traces(line_color='#A020F0', line_width=3)
    return fig
    

ano_filtrado = []
[ano_filtrado.append(x) for x in so_ano if x not in ano_filtrado]
ano_filtrado.append('Todos')

# =================GRÁFICO QUANTIDADE UNIDADES VENDIDAS ===========================================

def cria_grafico(dados_):

    return  px.scatter(dados_, x=1, y=2,
            size=2, color=0,hover_name=0,
            log_x=True, size_max=60, template ='plotly_dark')


#lê o arquivo csv e joga os dados em um variavel
dados = pd.read_csv('dados.csv', sep=',', encoding= 'unicode_escape')
dados = dados.values.tolist()
dados_filtrados = []

jogos = ["Minecraft",
         "Grand Theft Auto V",
         "PlayerUnknown's Battlegrounds",
         "Resident evil Series",
         "Red Dead Redemption 2",
         "Tomb Raider series"]

for x in dados:
    if x[0] in jogos:
        dados_filtrados.append(x)

#cria o gráfico
fig = cria_grafico(dados_filtrados) 

#unique
op = []
for x in dados_filtrados:
    if x[0] not in op:
        op.append(x[0])

op.append("all")

#=================GRÁFICO RELEVÂNCIA ENTRE JOGOS========================================

read_steam = pd.read_csv('Valve_Player_Data.csv')
list_steam = read_steam.values.tolist() #transformação matricial

def filter_with_time(value):
    ''' Função que recebe um valor em ano ou mês e retorna uma lista filtrando a dataBase Valve_player_data'''
    
    filter_time = []   #lista para receber os valores da filtragem
    
    #chave que servirá para analisar se o value é mes, ano ou inválido
    key = len([num for num in str(value)])  #Lê quantos elemntos compoe o caracter
    
    # se tiver quatro caracteres, é ano
    if key == 4:
        value = str(value) #str é referente a ano
        choice = 0 #essa escolha servirá para referenciar à coluna na filtragem
    
    #se tiver 2 caracteres e está entre 1 e 12 (meses), sendo válido para int
    elif key == 2 and int(value) <=12 and int(value) >=1:
        value = str(value) #str é referente a mês
        choice = 1
    
    else:    #não é valido para a filtragem
        return 'Resposta não validada'
    
    for line in list_steam:     #loop para cada linha da lista steam
        
        #no elemento 6, encontra-se a data em valor numérico (ex.: 2019-11-03)
        if line[6].split('-')[choice] == value:    #sempre que o valor pedido for equivalente ao requerido
            filter_time.append(line)   #add a linha do game (com todos os seus dados daquele mes) ao filtro
        
    
    filter_time.reverse()  #inverte a lista, pois o tempo está em ordem decrescente 
    return filter_time 

def pie_chart(filter_time, choice):
    ''' Função que recebe a lista filtrada por tempo e a escolha que será feita pelo usuário no frot, Retorna grafico '''
    
    #restringirá a análise para o desejado pelo usuário
    if choice == 'Pico de jogadores':  
        valores = [x[4] for x in filter_time] #referente ao pico de players  #index 4 na Database
        
    else:
        valores = [x[1] for x in filter_time] #x[1] referente a media de players   #index 1 na Database
        
    nomes = [x[7] for x in filter_time] #coluna que extrai os jogos no periodo de tempo analisado e coloca na lista 'nomes'
    
    fig= px.pie(values = valores, names= nomes, title = f'Relevância dos jogos: {choice}', color= nomes, labels= nomes,template='plotly_dark')
    fig.update_traces(textposition= 'inside')   #coloca as porcentagens dentro do gráfico
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode= 'hide')   #caso a fonte seja menor que 12, escondê-la
    
    return fig

# ==================================FRONT-END===========================================

# Layout 
app.layout = dbc.Container(
    children=[
        dbc.Row([
            dbc.Col([
                    html.Div(children=[
                        html.H3(children="ANÁLISE DE DADOS DA PLATAFORMA STEAM",
                        style={
                        "background-color": "#1E1E1E","padding":"40px"}),
                        html.H5(children="Avaliação dos jogos da Steam 1995-2021",style={"margin-top": "40px"}),
                        html.P(children="A avaliação da crítica advém das notas do site Metacritic que são calculadas com base na média ponderada de todas as críticas e avaliações das mídias especializadas cadastradas no site.",style={"margin-top": "40px"})],
                        style={"margin": "-25px", "padding": "25px"}),
                    html.P("Informe o jogo a qual deseja obter informações:", style={"margin-top": "20px"}),
                    dcc.Dropdown(
                                        todos_jogos, value='Half-Life 2',
                                        style={"margin-top": "10px"},id="location-dropdown"
                                    ),
                    dcc.Graph(id='grafico',
                        figure= criargrafico(jogos),
                        style={"background-color": "#1E1E1E"})],)
                ],style={"padding": "25px"
                          }),
                          dbc.Row([
                            html.Div(children=[
    html.H5(children='Análise do número de jogadores no período pandemico',style={"padding": "22px","margin-top": "20px"}),
    html.P(children='Obs: No caso de jogos lançados depois de 2019, será mostrado todos seus dados',style={"padding": "20px","margin-top": "5px"}),

    html.Div(children='''
       O gráfico escolhido foi: 
    ''', id = 'texto',style={"padding": "20px","padding-top": "5px"}),

    dcc.Dropdown(nome_filtrado, value='Counter Strike: Global Offensive', id='graficos'),
    dcc.Graph(
        id='Grafico_P',
        figure= dado_jogo('Counter Strike: Global Offensive'),style={"padding": "30px","margin-left": "25px"}
    ),
])]),dbc.Row([html.Div(children=[
    html.H5(children='Montante de jogadores anuais',style={"padding": "22px","margin-top": "20px"}),
    html.P(children='Análise dos jogadores de todos os jogos da database, as pontas criadas devem-se ao fato de certos jogos serem desproporcionalmente mais populares que outros.',style={"padding": "20px","margin-top": "5px"}),

    html.Div(children='''
       O ano escolhido foi: Todos
    ''', id = 'texto2',style={"padding": "20px","padding-top": "5px"}),

    dcc.Dropdown(ano_filtrado, value='Todos', id='graficos2'),
    dcc.Graph(
        id='Grafico_J',
        figure= todos('a'),style={"padding": "30px","margin-left": "25px"}
    )
])]),dbc.Row([html.Div([
    
    html.H5("Quantidade de unidades vendidas",style={"padding": "22px","margin-top": "20px"}),
    html.P('O intuito é mostrar a variação no número total de vendas de jogos específicos em comparação a várias séries de jogos, elucidando a relevância dos jogos.',style={"padding": "20px","margin-top": "5px"}),

    dcc.Dropdown(op, value="all", id='drop-op'),

    dcc.Graph(
        id='graph-sells',
        figure=fig
    )
])]),dbc.Row([html.Div(
    children = [
        html.H5('Relevancia entre jogos', style={"padding": "22px","margin-top": "20px"}),
        Div(id= 'period_text', children=[], style={"padding": "20px","margin-top": "10px"}),
        dcc.Dropdown(id= 'Drop_relevance', 
                 options= ['Pico de jogadores', 'Média de jogadores'] ,
                 value= 'Pico de jogadores'),
        html.P(style={"padding": "10px","margin-top": "5px"}),
        Slider(id= 'slider_time', min= 2012, max= 2021, step= 1, value= 2021, 
               tooltip={"placement": "bottom", "always_visible": True}), 
        Graph(id= 'grafico_relevancia', 
              figure= {})
    ]
    
)]),
    ],fluid=True, 
)

# =============CALLBACK GRÁFICO 1 =======================
@app.callback(
    Output("grafico",'figure'),
    Input('location-dropdown','value')
)

def update_output(value):
    list4 = []
    list4.append(value)
    return criargrafico(list4)

#===============CALLBACK GRÁFICO 2 =======================
@app.callback(
    Output('Grafico_P','figure'),
    Input('graficos','value')
)
def update_output(value):
    return dado_jogo(value)

@app.callback(
    Output('texto','children'),
    Input('graficos','value')
)
def update_output2(value):
    return f'O gráfico escolhido foi: {value}'

#================CALLBACK GRÁFICO 3==========================
@app.callback(
    Output('Grafico_J','figure'),
    Input('graficos2','value')
)
def update_output(value):
    if value == 'Todos':
        a = todos('x')
    else:
        #value = str(value)
        a = por_ano(str(value))
    return a

@app.callback(
    Output('texto2','children'),
    Input('graficos2','value')
)
def update_output2(value):
    return f'O ano escolhido foi: {value}'

#=============CALLBACK GRÁFICO 4==============================
@app.callback(
    Output(component_id='graph-sells', component_property='figure'),
    Input(component_id='drop-op', component_property='value')
)

def update_graph(input_value):

    if input_value == "all":
        
        fig = cria_grafico(dados_filtrados)

    else:

        dados2 = []
        for x in dados_filtrados:
            if x[0] == input_value:
                dados2.append(x)
        
        fig = cria_grafico(dados2)

    fig.update_yaxes(title= 'Vendas') #definindo titulo dos eixos 
    fig.update_xaxes(title= "Anos") #definindo titulo dos eixos
    fig.update_traces(hovertemplate=None)

    return fig

#==============CALLBACK GRÁFICO 5==========================
#output: valor que será modificado no layout
#input: escolha do usuário na modificação e análise
@app.callback(
    [Output('period_text','children'),         
    Output('grafico_relevancia', 'figure')],      
    [Input('Drop_relevance','value'),
     Input('slider_time','value')],
    )

def update_fig_relevancia(drop_value, value):
    ''' Função que recebe a escolha do tempo e do tipo de análise do usuário e retorna as modificações '''
    
    filter_period = filter_with_time(value)   #lista filtrada pelo tempo (segundo o requisitado)
    child = f"ano de {value}"      #modificação em texto referente ao ano
    
    fig= pie_chart(filter_period,drop_value)  #execução da função grafico
    
    return child, fig

if __name__ == "__main__":
    app.run_server(debug=False, port=8051)