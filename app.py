import datetime
import dash
import pandas as pd
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc


import pandas_datareader.data as data
start = datetime.datetime(2020,1,1)
end = datetime.datetime.today().date()
df = data.DataReader(['AMZN','AAPL','GOOGL','FB','MRNA','BA','TSLA','MSFT','V','MA'],'stooq',start=start,end=end)
df = df.stack().reset_index()
df.to_csv('stocks.csv',index=False)
df = pd.read_csv('stocks.csv')

from datetime import date, timedelta
current_date = date.today()
yesterday = current_date - timedelta(1)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ],
                meta_tags=[{'name':'viewport',
                            'content':'width=device-width, initial-scale=1.0'}])
server = app.server
app.title='Stock Price Analysis'
app.layout = dbc.Container([
    html.Br(),
    dbc.Card([
        html.H1('Stock Price Analysis',style={'text-align':'center','color':'black'}),
    ]),
    html.Br(),
# Row 1
    dbc.Row([
        dbc.Col([
            dbc.Card([

                html.H3('Single Stock',style={'text-align':'center','color':'black'})
            ]),
            html.Br(),
            dcc.Dropdown(id='my-dpdn', multi=False, value='AMZN', placeholder='Select one Stock...', optionHeight=20,
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())],
                         style={'color': 'black', 'background': 'white'}),
            html.Br(),
            dcc.Graph(id='line-graph', figure={})
        ],xs=12,sm=12,md=12,lg=5,xl=5,width={'offset':1}),
        dbc.Col([
            dbc.Card([
                html.H3('Multiple Stocks',style={'text-align':'center','color':'black'})
            ]),
            html.Br(),
            dcc.Dropdown(id='my-dpdn2', multi=True, value=['AMZN','AAPL'], placeholder='Select atleast one Stock...',
                         options=[{'label': x, 'value': x}
                                  for x in sorted(df['Symbols'].unique())
                                  ], style={'color': 'black', 'background': 'white', 'font-color': 'blue'}, ),
            html.Br(),
            dcc.Graph(id='line-graph2', figure={})
        ],xs=12,sm=12,md=12,lg=5,xl=5)
    ],justify='center'),
# Row 2
    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Graph(id='line-graph3', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5, width={'offset':1}),
        dbc.Col([
            html.Br(),
            dcc.Graph(id='line-graph4', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5)
    ],justify='center'),
# Row 3
    dbc.Row([
        dbc.Col([
            html.Br(),
            dcc.Graph(id='line-graph5', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5,width={'offset':1}),
        dbc.Col([
            html.Br(),
            dcc.Graph(id='line-graph6', figure={})
        ], xs=12, sm=12, md=12, lg=5, xl=5)
    ],justify='center'),

    html.Br(),
    dbc.Row([
        html.Br(),
        dbc.Card([
            html.H3('Thank You!!', style={'text-align': 'center', 'color': 'black'}),
        ]),
        ])

],fluid=True)

# graph 1
@app.callback(
    Output('line-graph','figure'),
    Input('my-dpdn','value')
)
def graph_update(x):
    dff = df[df['Symbols']==x]
    layout = go.Layout(title=f'Stock: {x}', xaxis=dict(title="Date"),
                       yaxis=dict(title="Price($)"),
                       template='plotly_dark',
                       xaxis_rangeslider_visible=False,
                       title_x=0.5)
    fig = go.Figure(data=[go.Candlestick(x=dff['Date'],
                                         open=dff['Open'], high=dff['High'],
                                         low=dff['Low'], close=dff['Close'], text=dff['Volume'])
                          ], layout=layout)
    return fig
# graph 2 callback for line chart- multiselect
@app.callback(
    Output('line-graph2','figure'),
    Input('my-dpdn2','value')
)
def update_graph1(stock_selected):
    dff = df[df['Symbols'].isin(stock_selected)]
    fig = px.line(dff,x='Date',y='High',color='Symbols',template='plotly_dark')
    fig.update_layout(title={'text': f'Multi Stocks Comparison: {stock_selected}', 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    return fig

# graph 3 callback for line chart- multiselect
@app.callback(
    Output('line-graph3','figure'),
    Input('my-dpdn','value')
)
def update_graph1(x):
    dff = df[df['Symbols']==x]
    fig = px.line(template='plotly_dark')
    fig.add_scatter(x=dff['Date'], y=dff['Open'], mode='lines', name='Open')
    fig.add_scatter(x=dff['Date'], y=dff['Low'], mode='lines', name='Low')
    fig.add_scatter(x=dff['Date'], y=dff['High'], mode='lines', name='High')
    fig.add_scatter(x=dff['Date'], y=dff['Close'], mode='lines', name='Close')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Price($)')
    fig.update_layout(title={'text': f"Open/High/Low/Close Comparison: {x}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    return fig
# graph 4 callback for histogram
@app.callback(
    Output('line-graph4','figure'),
    Input('my-dpdn2','value')
)
def update_graph2(stock_selected):
    dff = df[df['Symbols'].isin(stock_selected)]
    dff = dff[dff['Date']==yesterday.strftime('%Y-%m-%d')]
    fighist = px.histogram(dff,x='Symbols',y='Close',color='Symbols',template='plotly_dark')
    fighist.update_layout(
        title={'text': f"Close Price Comparison: {stock_selected}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fighist.update_xaxes(title_text='Stock')
    fighist.update_yaxes(title_text='Closed Price($) as on 2021-12-30')
    return fighist

# graph 5 callback for histogram
@app.callback(
    Output('line-graph5','figure'),
    Input('my-dpdn','value')
)
def update_graph2(stock_selected):
    fig = px.line(template='plotly_dark')
    fig.add_scatter(x=df['Date'], y=df[df['Symbols'] == stock_selected].High, mode='lines', name='High')
    fig.add_scatter(x=df['Date'], y=df[df['Symbols'] == stock_selected].Low, mode='lines', name='Low')
    fig.update_xaxes(title_text='Date')
    fig.update_yaxes(title_text='Close Price($)')
    fig.update_layout(
        title={'text': f"High and Low Price: {stock_selected}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})

    return fig

# graph 6 callback for histogram
@app.callback(
    Output('line-graph6','figure'),
    Input('my-dpdn2','value')
)
def update_graph2(stock_selected):
    dff = df[df['Symbols'].isin(stock_selected)]
    dff = dff[dff['Date'] == yesterday.strftime('%Y-%m-%d')]
    fig = px.pie(dff, names='Symbols', values='Volume', color='Symbols', template='plotly_dark',color_discrete_sequence=px.colors.qualitative.G10)
    fig.update_layout(
        title={'text': f"Stock Volume as on {yesterday.strftime('%Y-%m-%d')}", 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'})
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig

if __name__ == "__main__":
    app.run_server(debug=True)


