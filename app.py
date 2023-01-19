"""
A simple app demonstrating how to dynamically render tab content containing
dcc.Graph components to ensure graphs get sized correctly. We also show how
dcc.Store can be used to cache the results of an expensive graph generation
process so that switching tabs is fast.
"""
import time

import dash
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, dcc, html

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "AgeEst"

# Include the server option to become able to deploy online
server = app.server

SIDEBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "position": "fixed",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

set_of_variables = {
    "Suchey Brooks 1990": [
        'Right Phase Suchey',
    ],
    "Meindl and Lovejoy": [
        'Right 1-midlamdoid',
        '2-lambda',
        '3-obelion',
        '4-anterior sagital',
        '5-bregma',
        'Right 6-midcoronal',
        'Right 7-pterion',
        'Right 8-sphenofrontal',
        'Right 9-inferior sphenotemporal',
        'Right 10-superior sphenotemporal'
    ],
    "Lovejoy et al": [
        "Right Phase"
    ],
    "Buckberry and Chamberlain": [
        'Right Transverse organization',
        'Right Surface texture',
        'Right Microposity',
        'Right Macroporositty',
        'Right Apical changes'
    ],
    "Suchey Brooks 1990 and Lovejoy et al": [
        'Right Phase Suchey',
        'Right Phase'
    ],
    "Suchey Brooks 1990 and Buckberry Chamberlain": [
        'Right Transverse organization',
        'Right Surface texture',
        'Right Microposity',
        'Right Macroporositty',
        'Right Apical changes',
        'Right Phase Suchey'
    ],
    "All": [
        'Right Phase Suchey',
        'Right 1-midlamdoid',
        '2-lambda',
        '3-obelion',
        '4-anterior sagital',
        '5-bregma',
        'Right 6-midcoronal',
        'Right 7-pterion',
        'Right 8-sphenofrontal',
        'Right 9-inferior sphenotemporal',
        'Right 10-superior sphenotemporal',
        "Right Phase",
        'Right Transverse organization',
        'Right Surface texture',
        'Right Microposity',
        'Right Macroporositty',
        'Right Apical changes'
    ]
}

variables_ranges = {
    'Right Phase Suchey': [1, 6],
    'Right 1-midlamdoid': [0, 3],
    '2-lambda': [0, 3],
    '3-obelion': [0, 3],
    '4-anterior sagital': [0, 3],
    '5-bregma': [0, 3],
    'Right 6-midcoronal': [0, 3],
    'Right 7-pterion': [0, 3],
    'Right 8-sphenofrontal': [0, 3],
    'Right 9-inferior sphenotemporal': [0, 3],
    'Right 10-superior sphenotemporal': [0, 3],
    "Right Phase": [1, 8],
    'Right Transverse organization': [1, 5],
    'Right Surface texture': [1, 5],
    'Right Microposity': [1, 5],
    'Right Macroporositty': [1, 5],
    'Right Apical changes': [1, 5]
}


# print(variables_ranges['Right Apical changes'])

# print(list(vars.keys()))
# print("-------")
# print(list(vars["Suchey Brooks 1990 and Buckberry Chamberlain"]))


sidebar = html.Div(
    [
        html.H2("Input", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar where users can choose what they want to do", className="lead"
        ),
        dbc.Nav(
            [
                # dbc.NavLink("Home", href="/", active="exact"),
                # dbc.NavLink("Page 1", href="/page-1", active="exact"),
                # dbc.NavLink("Page 2", href="/page-2", active="exact"),
                dbc.DropdownMenu(
                    label="Select input variable set",
                    menu_variant="dark",
                    id='select-input-variable-set',
                    children=[
                        dbc.DropdownMenuItem(item, id=str(item)) for item in list(set_of_variables.keys())
                    ],
                    className="smaller-dropdown"
                )
            ],

            vertical=True,
            pills=True,
        ),
        dbc.Row(id='out-test')
    ],
    style=SIDEBAR_STYLE,
)


# dropdown = dbc.DropdownMenu(
#     label="Select input variable set",
#     menu_variant="dark",
#     id='select-input-variable-set',
#     children=[
#         dbc.DropdownMenuItem(item, id=str(item)) for item in list(set_of_variables.keys())
#     ]
# )

content = html.Div(id="page-content", style=CONTENT_STYLE)

# my_content = dbc.Container()


# app.layout = dbc.Container(
#     [
#         # dcc.Store(id="store"),
#         dcc.Location(id="url"),
#         sidebar,
#         content,
#         html.H1("AgeEst, an age estimation web app"),
#         html.Hr(),
#         #dropdown,
#         html.Br(),
#         dbc.Row(id='output-container'),
#         html.Hr()
#     ],
#     style=CONTENT_STYLE
# )

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    # Output('output-container', 'children'),
    Output('out-test', 'children'),
    [Input(str(item), 'n_clicks') for item in list(set_of_variables.keys())]
)
def update_form(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    # print(button_id)

    if button_id in list(set_of_variables.keys()):

        element_to_insert = dbc.Input(type="number", min=0, max=10, step=1)

        element = dbc.Row([
            dbc.Label(item) for item in list(set_of_variables[str(button_id)])
        ])

        # print("xxx")
        # print(list(set_of_variables[str(button_id)]))
        # print("xxx")

        # print(
        #     [dbc.Input(
        #         type="number", min=0, max=10, step=1) for item in list(set_of_variables[str(button_id)])
        #      ])

        # for item in list(set_of_variables[str(button_id)]):
        #     print(item)
        #     print(variables_ranges[item][1])

        # print(element.children.append(dbc.Input(type="number", min=0, max=10, step=1)))

        # print(element.children[0])
        # print(len(element.children))

        # my_list = [1, 2, 3, 4, 5]
        # element_to_insert = 0

        for i in range(1, 2*len(element.children)+1, 2):
            # print(i)
            element.children.insert(i, dbc.Input(
                type="number", min=0, max=10, step=1))

        # element.children.append(element_to_insert)

        # print(vars(list))
        # element.children.append(dbc.Input(type="number", min=0, max=10, step=1))

        # print("xxx")
        # for child in element.children:
        #     child = [child, dbc.Input(type="number", min=0, max=10, step=1)]
        #     print(child)
        #     #child.append(dbc.Input(type="number", min=0, max=10, step=1))

        # print("xxx")

        # dbc.Input(type="number", min=0, max=10, step=1)

        return element
    else:
        return ''


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(debug=True)
