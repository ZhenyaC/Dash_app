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

ig_deals_cleaned = pd.read_csv("../multipage-dash-app/preprocessed.csv", low_memory=False)
ig_deals_cleaned['Nic']=pd.to_numeric(ig_deals_cleaned['Nic'], errors='coerce')
month_stats = ig_deals_cleaned.groupby(['month','IssuerBorrowerType']).agg({'Size_m': 'sum'}).reset_index().set_index('month')
#weekly_vols = ig_deals_cleaned.groupby(['week','IssuerBorrowerType']).agg({'Size_m': 'sum'}).reset_index().set_index('week')
weekly_vols =ig_deals_cleaned.groupby('week').agg({'Book_Size': 'sum','Size_m': 'sum', 'tranche_bk_to_cvr':'mean', 'Nic':'mean'}).reset_index()
annual_vols= ig_deals_cleaned.groupby('year').agg({'Size_m': 'sum'})
daily_vols = ig_deals_cleaned.groupby('PricingDate')['Size_m'].sum()

CHART_THEME = "plotly_white"
m_chart = px.bar(x=month_stats.tail(30).index, y=month_stats.tail(30)['Size_m']*1e3, labels=dict(x ="Month", y="Volume $US"), template = "plotly_white")

annual_chart =px.bar(x = annual_vols.index, y=annual_vols['Size_m']*1e6, labels=dict(x ="Year", y="Volume $US"), template = "plotly_white")


# Create figure with secondary y-axis
weekly_fig = make_subplots(specs=[[{"secondary_y": True}]])
weekly_fig.layout.template = CHART_THEME
# Add traces
weekly_fig.add_trace(
    go.Bar(x=weekly_vols.tail(20).index, y=weekly_vols.tail(20)['Size_m']*1e5, name="Volume US$"),
    secondary_y=False,
)
weekly_fig.add_trace(
    go.Scatter(x=weekly_vols.tail(20).index, y=weekly_vols.tail(20)['Nic'], name="New Issue Concession (bp)"),
    secondary_y=True,
)

weekly_fig.layout.height=500
weekly_fig.update_layout(margin = dict(t=50, b=50, l=25, r=25))  # optm the chart space

weekly_fig.update_layout(
    #title='Weekly Volumes and Weekly Average Book To Cover',
    xaxis=dict(tickmode = 'array', tickvals = weekly_vols.index, ticktext = weekly_vols['week']),
    yaxis=dict(
        title='Value:$US',
        titlefont_size=14,
        tickfont_size=12,
        ))

### Add the page components here 
table_header = [
    html.Thead(html.Tr([html.Th("First Name"), html.Th("Last Name")]))
]

row1 = html.Tr([html.Td("Arthur"), html.Td("Dent")])
row2 = html.Tr([html.Td("Ford"), html.Td("Prefect")])
row3 = html.Tr([html.Td("Zaphod"), html.Td("Beeblebrox")])
row4 = html.Tr([html.Td("Trillian"), html.Td("Astra")])

table_body = [html.Tbody([row1, row2, row3, row4])]

page2_table = dbc.Table(table_header + table_body, bordered=True)


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
                      figure=weekly_fig,
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
                      figure=m_chart,
                      style={'height':380}),
            ], width={'size': 7, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on third row
                html.H5('ANNUAL VOLUMES (US$)', className='text-center'),
                dcc.Graph(id='pie-top15',
                      figure = annual_chart,
                      style={'height':380}),
            ], width={'size': 5, 'offset': 0, 'order': 2}),  # width second column on second row
        ])  # end of third row
        
    ], fluid=True)
