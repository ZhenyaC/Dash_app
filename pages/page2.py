# Import necessary libraries 
import dash
from dash import html, Dash, dash_table, Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#from jupyter_dash import JupyterDash
import plotly.io as pio

ig_deals_cleaned = pd.read_csv("data/us_ig_cleaned.csv", low_memory=False)
ig_deals_cleaned['Nic']=pd.to_numeric(ig_deals_cleaned['Nic'], errors='coerce')
month_stats = ig_deals_cleaned.groupby(['month','IssuerBorrowerType']).agg({'Size_m': 'sum'}).reset_index().set_index('month')
#weekly_vols = ig_deals_cleaned.groupby(['week','IssuerBorrowerType']).agg({'Size_m': 'sum'}).reset_index().set_index('week')
weekly_vols =ig_deals_cleaned.groupby('week').agg({'Book_Size': 'sum','Size_m': 'sum', 'tranche_bk_to_cvr':'mean', 'Nic':'mean'}).reset_index()
annual_vols= ig_deals_cleaned.groupby('year').agg({'Size_m': 'sum'})
daily_vols = ig_deals_cleaned.groupby('PricingDate')['Size_m'].sum()

CHART_THEME = "plotly_white"
m_chart = px.bar(x=month_stats.tail(30).index, y=month_stats.tail(30)['Size_m']*1e6, labels=dict(x ="Month", y="Volume $US"), template = "plotly_white")

annual_chart =px.bar(x = annual_vols.index, y=annual_vols['Size_m']*1e6, labels=dict(x ="Year", y="Volume $US"), template = "plotly_white")


# Create figure with secondary y-axis
weekly_fig = make_subplots(specs=[[{"secondary_y": True}]])
weekly_fig.layout.template = CHART_THEME
# Add traces
weekly_fig.add_trace(
    go.Bar(x=weekly_vols.tail(20).index, y=weekly_vols.tail(20)['Size_m']*1e6, name="Volume US$"),
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

##Indicators Data
summaries = ig_deals_cleaned
summaries['PricingDate'] = pd.to_datetime(summaries['PricingDate'])
summaries=summaries.set_index('PricingDate')
todays_count = summaries.sort_values('PricingDate', ascending=True).resample('d').count()['DealId'].tail(1)
today_vols = summaries.sort_values('PricingDate', ascending=True).resample('d').sum()['Size_m'].tail(1)
th_week = summaries.sort_values('PricingDate', ascending=True).resample('W').sum()['Size_m'].tail(1)
th_month=summaries.sort_values('PricingDate', ascending=True).resample('M').sum()['Size_m'].tail(1)
th_quarter = summaries.sort_values('PricingDate', ascending=True).resample('Q').sum()['Size_m'].tail(1)
this_ytd = summaries.sort_values('PricingDate', ascending=True).resample('A').sum()['Size_m'].tail(1)
full_year_ly =summaries.sort_values('PricingDate', ascending=True).resample('A').sum()['Size_m'].get(-2)
today = pd.to_datetime('now')
today_last_year = today - pd.Timedelta(365, "day")
last_year_td = summaries[(summaries.index >= '2021-01-01') & (summaries.index <= today_last_year)]['Size_m'].cumsum().tail(1)

indicators_ptf = go.Figure()
indicators_ptf.layout.template = CHART_THEME
indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = int(todays_count),
    #number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Today's Count</span>"},
    #delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 0, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(today_vols))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Today's Issuance</span>"},
    #delta = {'position': "bottom", 'reference': 1, 'relative': False},
    domain = {'row': 1, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(th_week))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Weekly Issuance</span>"},
    #delta = {'position': "bottom", 'reference': 2, 'relative': False},
    domain = {'row': 2, 'column': 0}))

indicators_ptf.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(th_month))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Monthly Issuance</span>"},
    #delta = {'position': "bottom", 'reference': 3, 'relative': False},
    domain = {'row': 3, 'column': 0}))


indicators_ptf.update_layout(
    grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)

indicators = go.Figure()
indicators.layout.template = CHART_THEME
indicators.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(th_quarter))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Quarterly Issuance</span>"},
    #delta = {'position': "bottom", 'reference': 0, 'relative': False},
    domain = {'row': 0, 'column': 0}))

indicators.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(this_ytd))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>This YTD</span>"},
    #delta = {'position': "bottom", 'reference': 1, 'relative': False},
    domain = {'row': 1, 'column': 0}))

indicators.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(last_year_td))/1000,
    number = {'suffix': " bn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Last YTD</span>"},
    #delta = {'position': "bottom", 'reference': 2, 'relative': False},
    domain = {'row': 2, 'column': 0}))

indicators.add_trace(go.Indicator(
    mode = "number+delta",
    value = (float(full_year_ly))/1000000,
    number = {'suffix': " trn"},
    title = {"text": "<br><span style='font-size:0.7em;color:gray'>Full Year Last Year</span>"},
    #delta = {'position': "bottom", 'reference': 3, 'relative': False},
    domain = {'row': 3, 'column': 0}))


indicators.update_layout(
    grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
    margin=dict(l=50, r=50, t=30, b=30)
)

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
                      figure=indicators_ptf,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 2, 'offset': 0, 'order': 2}),  # width second column on second row
            dbc.Col([  # third column on second row
            html.H5('OTHER STATS', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      figure=indicators,
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
