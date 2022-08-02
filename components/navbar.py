# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Scorecard", href="/page1")),
                dbc.NavItem(dbc.NavLink("Trends", href="/page2")),
                dbc.NavItem(dbc.NavLink("Summaries", href="/page3"))
            ] ,
            brand="DEBT ANALYTICS",
            brand_href="/page1",
            color="dark",
            dark=True,
        ), 
    ])

    return layout
