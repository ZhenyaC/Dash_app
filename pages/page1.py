# Import necessary libraries 
from dash import html, Dash, dash_table, Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from jupyter_dash import JupyterDash
import plotly.io as pio
from plotly import figure_factory as ff

ig_deals_cleaned = pd.read_csv('../multipage-dash-app/us_ig_cleaned.csv', low_memory=False)

quarterly_stats = ig_deals_cleaned.groupby('quarter').agg({'Size_m': 'sum'}).reset_index().set_index('quarter')


sectors_q = ig_deals_cleaned[(ig_deals_cleaned['quarter'] == '2021Q2') | (ig_deals_cleaned['quarter'] == '2022Q2')].groupby(['quarter','Sector'])['Size_m'].sum().sort_values(ascending = False).to_frame().reset_index().rename(columns = {0: 'Amount'}).sort_values('Size_m')
sectors_q=sectors_q.sort_values('Size_m', ascending = False)

sectors_q = ig_deals_cleaned[(ig_deals_cleaned['quarter'] == '2021Q2') | (ig_deals_cleaned['quarter'] == '2022Q2')].groupby(['quarter','Sector'])['Size_m'].sum().sort_values(ascending = False).to_frame().reset_index().rename(columns = {0: 'Amount'}).sort_values('Size_m')
sectors_q=sectors_q.sort_values('Size_m', ascending = False)
sectors_graph = sectors_q.pivot(index='Sector', columns='quarter', values='Size_m').sort_values(by='2022Q2', ascending =False)

esg = ig_deals_cleaned.loc[(ig_deals_cleaned['ESG'] ==True) | (ig_deals_cleaned['ESG Type'].notnull()), ['PricingDate', 'quarter','month', 'year', 'week','DealIssuer', 'Sector', 'ESG Type', 'Size_m']].set_index('quarter')
esg_q_stats = esg.groupby(['quarter','ESG Type']).agg({'Size_m': 'sum'}).reset_index().set_index('quarter')


CHART_THEME = "plotly_white"
### TOP 10 SECTORS
# Create figure with secondary y-axis
sectors_fig = make_subplots(specs=[[{"secondary_y": True}]])


# Add traces
sectors_fig.add_trace(
    go.Bar(x=sectors_graph.head(10)['2022Q2']*1e5, y=sectors_graph.head(10).index, name="2022 Q2", orientation="h")
)
sectors_fig.add_trace(
    go.Bar(x=sectors_graph.head(10)['2021Q2']*1e5, y=sectors_graph.head(10).index,name="2021 Q2", orientation="h")
)
# Add figure title
sectors_fig.layout.template = CHART_THEME

sectors_fig.update_layout(
    barmode ="group",
    margin = dict(t=50, b=50, l=25, r=25)
)


# Set x-axis title
sectors_fig.update_xaxes(title_text="Sectors")
sectors_fig.update_yaxes(autorange="reversed")


#sectors_fig.show()

###QUARTERLY VOLUMES

CHART_THEME = 'plotly_white'  # and try plotly_dark

chart_q = go.Figure()  # generating a figure that will be updated in the following lines
chart_q.add_trace(go.Bar(x=quarterly_stats.index, y=quarterly_stats['Size_m']*1e6,
                    name='Global Value'))
chart_q.layout.template = CHART_THEME
chart_q.layout.height=500
chart_q.update_layout(margin = dict(t=50, b=50, l=25, r=25))  # optm the chart space
chart_q.update_layout(
    #title='Quarterly Volume (USD $)',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value:$US',
        titlefont_size=14,
        tickfont_size=12,
        ))
# chart_ptfvalue.update_xaxes(rangeslider_visible=False)
# chart_ptfvalue.update_layout(showlegend=False)
#chart_q.show()

### ESG VOLUMES
fig2 = go.Figure(data=[
   go.Bar(name='ESG_q', x=esg_q_stats.index, y=esg_q_stats['Size_m']*1e6)
    #go.Bar(name='SP500', x=plotlydf_portfval['date'], y=plotlydf_portfval['sp500_pctch'])
])


# Change the bar mode
fig2.update_layout(barmode='group')
fig2.layout.template = CHART_THEME
fig2.layout.height=300
fig2.update_layout(margin = dict(t=50, b=50, l=25, r=25))
fig2.update_layout(
#     title='% variation - Portfolio vs SP500',
    xaxis_tickfont_size=12,
    yaxis=dict(
        title='Value:$US',
        titlefont_size=14,
        tickfont_size=12,
        ))
fig2.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.99))

ytd = pd.read_csv('../multipage-dash-app/ig_ytd.csv', low_memory=False)
ytd['PricingDate']=pd.to_datetime(ytd['PricingDate'])
top10_ytd = ytd.loc[ytd['IssuerBorrowerType']!= 'FIG'].groupby(['PricingDate','DealIssuer']).agg({'Size_m': 'sum'}).sort_values('Size_m', ascending =False).nlargest(10, 'Size_m').reset_index().rename(columns={'PricingDate': 'DATE', 'DealIssuer':'ISSUER','Size_m': 'USD AMOUNT'})
top10_ytd['USD AMOUNT']=top10_ytd['USD AMOUNT'].map('${:,.0f}'.format)
top10_ytd['DATE']=top10_ytd['DATE'].map('{:%Y-%m-%d}'.format)
fig_top10_ytd = ff.create_table(top10_ytd)

#fig2.show()

# Define the page layout
#layout = dbc.Container([
#    dbc.Row([
#        html.Center(html.H1("Page 1")),
#        html.Br(),
#       html.Hr(),
#       dbc.Col([
#           html.P("This is column 1."), 
#           dbc.Button("Test Button", color="primary")
#       ]), 
#       dbc.Col([
#           html.P("This is column 2."), 
#           html.P("You can add many cool components using the bootstrap dash components library."),
#       ])
#   ])
#])



layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('US IG DEBT TRENDS', className='text-center text-primary, mb-3'))),  # header row
        
        dbc.Row([  # start of second row
            dbc.Col([  # first column on second row
            html.H5('QUARTELY VOLUMES ($USD)', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      figure=chart_q,
                      style={'height':550}),
            html.Hr(),
            ], width={'size': 7, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on second row
            html.H5('TOP TEN SECTORS', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      figure=sectors_fig,
                      style={'height':550}),
            html.Hr()
            ], width={'size': 5, 'offset': 0, 'order': 2}),  # width second column on second row
           # dbc.Col([  # third column on second row
           # html.H5('S&P500', className='text-center'),
          #  dcc.Graph(id='indicators-sp',
          #            figure=chart_q,
          #            style={'height':550}),
          #  html.Hr()
        #    ], width={'size': 2, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row
        
        dbc.Row([  # start of third row
            dbc.Col([  # first column on third row
                html.H5('ESG SUSTAINABLE GREEN', className='text-center'),
                dcc.Graph(id='chrt-portfolio-secondary',
                      figure=fig2,
                      style={'height':380}),
            ], width={'size': 7, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on third row
                html.H5('LARGEST DEALS', className='text-center'),
                dcc.Graph(id='pie-top15',
                          responsive=True,
                      figure = fig_top10_ytd,
                      style={'height':380}),
            ], width={'size': 5, 'offset': 0, 'order': 2}),  # width second column on second row
        ])  # end of third row
        
    ], fluid=True)