# Import necessary libraries 
import dash
from dash import html, Dash, dash_table, Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash
import plotly.io as pio



# Define the final page layout
#layout = dbc.Container([
#    dbc.Row([
#        html.Center(html.H1("Page 2")),
#        html.Br(),
#        html.Hr(),
#        dbc.Col([
#            html.P("This is column 1."), 
#            dbc.Button("Test Button", color="secondary")
#        ]), 
#        dbc.Col([
#            html.P("This is column 2."), 
#            page2_table
#        ])
#    ])
#])



layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('DEBT TRENDS-OVER DIFFERNET TIME PERIODS', className='text-center text-primary, mb-3'))),  # header row
        
        dbc.Row([  # start of second row
            dbc.Col([  # first column on second row
            html.H5('WEEKLY VOLUMES ($US)', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      #figure=weekly_fig,
                      style={'height':550}),
            html.Hr(),
            ], width={'size': 8, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on second row
            html.H5('MORE STATS', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      #figure=indicators_ptf,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 2}),  # width second column on second row
            dbc.Col([  # third column on second row
            html.H5('OTHER STATS', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      #figure=indicators,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row
        
        dbc.Row([  # start of third row
            dbc.Col([  # first column on third row
                html.H5('DEBT ADDED BY MONTH (US$)', className='text-center'),
                dcc.Graph(id='chrt-portfolio-secondary',
                      #figure=m_chart,
                      style={'height':380}),
            ], width={'size': 7, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on third row
                html.H5('ANNUAL VOLUMES (US$)', className='text-center'),
                dcc.Graph(id='pie-top15',
                      #figure = annual_chart,
                      style={'height':380}),
            ], width={'size': 5, 'offset': 0, 'order': 2}),  # width second column on second row
        ])  # end of third row
        
    ], fluid=True)
