# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc


# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Page 1", href="/page1")),
                dbc.NavItem(dbc.NavLink("Page 2", href="/page2")),
                dbc.NavItem(dbc.NavLink("Page 3", href="/page3"))
            ] ,
            brand="DEBT ANALYTICS",
            brand_href="/page1",
            color="dark",
            dark=True,
        ), 
    ])

    return layout
