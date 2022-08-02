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
import plotly.figure_factory as ff
import numpy as np

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

ytd = pd.read_csv('data/ig_ytd.csv', low_memory=False)
hist_ig = pd.read_csv('data/us_ig_cleaned.csv', low_memory=False)

#change date to dtype datetime64[ns]
ytd['PricingDate']=pd.to_datetime(ytd['PricingDate'])
this_week=ytd.set_index('PricingDate')

weekly_total=this_week.sort_values('PricingDate', ascending=True).resample('W')[['Size_m','DealId']].agg({'Size_m':'sum', 'DealId':'count'}).tail(1)

weekly_total['Size_m']=weekly_total['Size_m'].map('${:,.0f}'.format)

this_week_total = weekly_total.reset_index().rename(columns={'PricingDate': '2022 YTD', 'DealId':'TRANCHES','Size_m': 'VOLUME'})
this_week_total['2022 YTD'].iloc[0] = "This Week"

fig_weekly_total = ff.create_table(this_week_total)

ytd_by_month = ytd.groupby('month').agg({'DealId': 'count','Size_m': 'sum'}).reset_index().rename(columns={'month': 'MONTH', 'DealId':'TRANCHES','Size_m': 'VOLUME'})
ytd_by_month['VOLUME']=ytd_by_month['VOLUME'].map('${:,.0f}'.format)


fig_ytd_by_month=ff.create_table(ytd_by_month)

issuer_type = ['FIG', 'Corporate']
ytd_corp_fin = ytd[ytd['IssuerBorrowerType'].isin(issuer_type)].groupby(['month','IssuerBorrowerType']).agg({'Size_m': 'sum'}).reset_index().rename(columns={'month': 'MONTH', 'IssuerBorrowerType':'IssuerBorrowerType','Size_m': 'VOLUME'})

ytd_corp_fin['VOLUME']=ytd_corp_fin['VOLUME'].map('${:,.0f}'.format)
ytd_corp_fin_month = ytd_corp_fin.pivot(index='MONTH',columns='IssuerBorrowerType', values='VOLUME').rename_axis(None, axis=1).reset_index()
fig_ytd_corp_fin_month = ff.create_table(ytd_corp_fin_month)

include_tenor = [2, 3, 4, 5, 7, 10, 30]
ratings_maturity =ytd[ytd['Tenor'].isin(include_tenor)][['Size_m', 'ratings', 'normalized_tenor']].groupby(['ratings', 'normalized_tenor'])['Size_m'].sum().reset_index()

ratings_maturity['Size_m'] =ratings_maturity['Size_m'].map('${:,.0f}'.format)
ratings_maturity_tab = ratings_maturity.pivot(index='normalized_tenor', columns ='ratings', values='Size_m').rename_axis(None, axis=1).reset_index().rename(columns={'normalized_tenor': 'TENOR', '0':'0','A': 'A AMOUNT', 'AA': 'AA AMOUNT', 'AAA': 'AAA AMOUNT', 'BBB':'BBB AMOUNT'})
ratings_maturity_tab=ratings_maturity_tab.fillna(0)

column_order = ['TENOR','AAA AMOUNT', 'AA AMOUNT', 'A AMOUNT', 'BBB AMOUNT']

ratings_maturity_reordered = ratings_maturity_tab.reindex(column_order, axis=1)
fig_ratings_mat = ff.create_table(ratings_maturity_reordered)

ytd['Nic'] = pd.to_numeric(ytd['Nic'], errors='coerce')
ytd_nic_book = ytd[['month', 'Nic', 'tranche_bk_to_cvr']].groupby('month').agg({'Nic':'mean','tranche_bk_to_cvr':'mean'}).round(2).reset_index().rename(columns={'month': 'MONTH', 'Nic':'AVG NIC ','tranche_bk_to_cvr': 'AVG BOOK TO COVER'})

fig_ytd_nic_book = ff.create_table(ytd_nic_book)
fig_ytd_nic_book.update_layout(autosize=False)

top20_ever = hist_ig.groupby(['PricingDate','DealIssuer']).agg({'Size_m': 'sum'}).sort_values('Size_m', ascending =False).nlargest(20, 'Size_m').reset_index().rename(columns={'PricingDate': 'DATE', 'DealIssuer':'ISSUER','Size_m': 'USD AMOUNT'})
fig_largest_ever = ff.create_table(top20_ever)


top10_ytd = ytd.loc[ytd['IssuerBorrowerType']!= 'FIG'].groupby(['PricingDate','DealIssuer']).agg({'Size_m': 'sum'}).sort_values('Size_m', ascending =False).nlargest(10, 'Size_m').reset_index().rename(columns={'PricingDate': 'DATE', 'DealIssuer':'ISSUER','Size_m': 'USD AMOUNT'})
top10_ytd['USD AMOUNT']=top10_ytd['USD AMOUNT'].map('${:,.0f}'.format)
top10_ytd['DATE']=top10_ytd['DATE'].map('{:%Y-%m-%d}'.format)
fig_top10_ytd = ff.create_table(top10_ytd)
new_layouts = {
    -0.45: -0.45,
    0.55: 0.10,
    1.55: 1.65
}
for annotation in fig_top10_ytd.layout['annotations']:
    annotation['x'] = new_layouts[annotation['x']]

fig_top10_ytd.layout['xaxis']['tickmode'] = 'array'
fig_top10_ytd.layout['xaxis']['tickvals'] = [x-0.05 for x in new_layouts.values()]

#ggg=dash_table.DataTable(
#    data=top10_ytd.to_dict('records'),
#    columns=[{'id': c, 'name': c} for c in top10_ytd.columns],
#    style_data={
#        'whiteSpace': 'normal',
#        'height': 'auto',
#    },
#    fill_width=False)

layout = dbc.Container(
    [
        dbc.Row(dbc.Col(html.H2('2022 SNAPSHOT', className='text-center text-primary, mb-3'))),  # header row
        
        dbc.Row([  # start of second row
            dbc.Col([ # first column on second row
            html.H5('THIS WEEK (Value $m)', className='text-center'),
            dcc.Graph(id='chrt-portfolio-main',
                      responsive=True,
                      figure=fig_weekly_total,
                      style={'height':150}),
            html.Hr(),
            ], width={'size': 4, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on second row
            html.H5('2022 ISSUANCE BY MONTH (Value $m)', className='text-center'),
            dcc.Graph(id='indicators-ptf',
                      responsive=True,
                      figure=fig_ytd_by_month,
                      style={'height':300}),
            html.Hr()
            ], width={'size': 4, 'offset': 0, 'order': 2}),  # width second column on second row
            dbc.Col([  # third column on second row
            html.H5('2022 CORP & FIG (Value $m)', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      responsive=True,
                      figure=fig_ytd_corp_fin_month,
                      style={'height':300}),
            html.Hr()
            ], width={'size': 4, 'offset': 0, 'order': 3}),  # width third column on second row
        ]),  # end of second row
        
        dbc.Row([  # start of third row
            dbc.Col([  # first column on third row
                html.H5('2022 ISSUANCE BY MATURITIES/RATINGS (Value $m)', className='text-center'),
                dcc.Graph(id='chrt-portfolio-secondary',
                          responsive=True,
                      figure=fig_ratings_mat,
                      style={'height':300}),
            ], width={'size': 4, 'offset': 0, 'order': 1}),  # width first column on second row
            dbc.Col([  # second column on third row
                html.H5('2022 AVERAGE NIC/BOOKS', className='text-center'),
                dcc.Graph(id='pie-top15',
                          responsive=True,
                      figure = fig_ytd_nic_book,
                      style={'height':300}),
            ], width={'size': 4, 'offset': 0, 'order': 2}),  # width second column on second row
            dbc.Col([  # third column on second row
            html.H5('2022 TOP TEN LARGEST DEALS (Value $m)', className='text-center'),
            dcc.Graph(id='indicators-sp',
                      responsive=True,
                      figure=fig_top10_ytd,
                      style={'height':300}),
            html.Hr()
            ], width={'size': 4, 'offset': 0, 'order': 3}),  # width third column on second row
        ])  # end of third row
        
    ], fluid=True)
