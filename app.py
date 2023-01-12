# # Run this app with `python app.py` and
# # visit http://127.0.0.1:8050/ in your web browser.


# # -----------------------------------------------------------------------
# # Import libraries

# import dash
# from dash import Dash, dcc, html, Input, Output
# import dash_bootstrap_components as dbc
# import pickle
# import tensorflow as tf
# import plotly.express as px
# import pandas as pd
# import pickle
# import numpy as np

# # -----------------------------------------------------------------------
# # Data related operations


# # -----------------------------------------------------------------------
# # Create the app

# app = Dash("__name__")
# app.title = "AgeEst"
# server = app.server

# vars = {
#     "Suchey Brooks 1990": [
#         'Right Phase Suchey'
#         ],
#     "Meindl and Lovejoy": [
#         'Right 1-midlamdoid',
#         '2-lambda',
#         '3-obelion',
#         '4-anterior sagital',
#         '5-bregma',
#         'Right 6-midcoronal',
#         'Right 7-pterion',
#         'Right 8-sphenofrontal',
#         'Right 9-inferior sphenotemporal',
#         'Right 10-superior sphenotemporal'
#         ],
#     "Lovejoy et al": [
#         "Right Phase"
#     ],
#     "Buckberry and Chamberlain": [
#         'Right Transverse organization',
#         'Right Surface texture',
#         'Right Microposity',
#         'Right Macroporositty',
#         'Right Apical changes'
#         ],
#     "Suchey Brooks 1990 and Lovejoy et al": [
#         'Right Phase Suchey',
#         'Right Phase'
#     ],
#     "Suchey Brooks 1990 and Buckberry Chamberlain": [
#         'Right Transverse organization',
#         'Right Surface texture',
#         'Right Microposity',
#         'Right Macroporositty',
#         'Right Apical changes',
#         'Right Phase Suchey'
#     ],
#     "All": [
#         'Right Phase Suchey',
#         'Right 1-midlamdoid',
#         '2-lambda',
#         '3-obelion',
#         '4-anterior sagital',
#         '5-bregma',
#         'Right 6-midcoronal',
#         'Right 7-pterion',
#         'Right 8-sphenofrontal',
#         'Right 9-inferior sphenotemporal',
#         'Right 10-superior sphenotemporal',
#         "Right Phase",
#         'Right Transverse organization',
#         'Right Surface texture',
#         'Right Microposity',
#         'Right Macroporositty',
#         'Right Apical changes',
#         'Right Phase Suchey',
#         'Right Phase',
#         'Right Transverse organization',
#         'Right Surface texture',
#         'Right Microposity',
#         'Right Macroporositty',
#         'Right Apical changes',
#         'Right Phase Suchey'
#     ]
# }

# #print(vars)

# # -----------------------------------------------------------------------
# # Create the layout of the app -- inludes all dash components (graphs, dropdowns, checkboxes)
# # and any html we need in our app

# app.layout = html.Div([
#     html.H1(
#         'AgeEst is an age estimation app',
#         style={
#             'color': 'black',
#             'background-color': 'cyan',
#             'padding': '10px'
#         }
#     ),
#     dcc.Dropdown(
#         id = 'select-set-of-input-variables',
#         options= list(vars.keys())
#     )
#     ,
#     html.Div([
#         html.Label('Model Type'),
#         dcc.Dropdown(
#             id='model-type-dropdown',
#             options=[
#                 {'label': 'Scikit-learn', 'value': 'scikit'},
#                 {'label': 'TensorFlow Keras', 'value': 'keras'}
#             ],
#             value='scikit'
#         )
#     ])
#     #,
#     # html.Div([
#     #     html.Label('Model File'),
#     #     dcc.Input(id='model-file-input', type='text', value='model.pkl')
#     # ]),
#     # html.Div([
#     #     html.Label('Input 1'),
#     #     dcc.Dropdown(
#     #         id='input-1-dropdown',
#     #         options=[
#     #             {'label': 'Value 1', 'value': 1},
#     #             {'label': 'Value 2', 'value': 2},
#     #             {'label': 'Value 3', 'value': 3},
#     #             {'label': 'Value 4', 'value': 4},
#     #         ],
#     #         value=1
#     #     )
#     # ]),
#     # html.Div([
#     #     html.Label('Input 2'),
#     #     dcc.Dropdown(
#     #         id='input-2-dropdown',
#     #         options=[
#     #             {'label': 'Value 1', 'value': 1},
#     #             {'label': 'Value 2', 'value': 2},
#     #             {'label': 'Value 3', 'value': 3},
#     #             {'label': 'Value 4', 'value': 4},
#     #         ],
#     #         value=1
#     #     )
#     # ]),
#     # html.Div([
#     #     html.Label('Input 3'),
#     #     dcc.Dropdown(
#     #         id='input-3-dropdown',
#     #         options=[
#     #             {'label': 'Value 1', 'value': 1},
#     #             {'label': 'Value 2', 'value': 2},
#     #             {'label': 'Value 3', 'value': 3},
#     #             {'label': 'Value 4', 'value': 4},
#     #         ],
#     #         value=1
#     #     )
#     # ]),
#     # html.Div([
#     #     html.Label('Input 4'),
#     #     dcc.Dropdown(
#     #         id='input-4-dropdown',
#     #         options=[
#     #             {'label': 'Value 1', 'value': 1},
#     #             {'label': 'Value 2', 'value': 2},
#     #             {'label': 'Value 3', 'value': 3},
#     #             {'label': 'Value 4', 'value': 4},
#     #         ],
#     #         value=1
#     #     )
#     # ])
# ])

# # -----------------------------------------------------------------------
# # Callbacks
# # Callbacks connect the component ids with the component property
# # A callback has an Output and an Input and comes with an accompanying funciton

# # @app.callback(
# #     Output('dd-output-container', 'children'),
# #     Input('demo-dropdown', 'value')
# # )

# # print(help(dash.html.H1))

# # Create a function to load the model


# def load_model(model_type, model_file):
#     if model_type == 'scikit':
#         with open(model_file, 'rb') as f:
#             model = pickle.load(f)
#     elif model_type == 'keras':
#         model = tf.keras.models.load_model(model_file)
#     return model


# if __name__ == '__main__':
#     app.run_server(debug=True)

# from dash import Dash, dcc, html, Input, Output

# app = Dash(__name__)
# app.layout = html.Div([
#     dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
#     html.Div(id='dd-output-container', children = [])
# ])


# @app.callback(
#     Output('dd-output-container', 'children'),
#     Input('demo-dropdown', 'value')
# )
# def update_output(value):
#     return f'You have selected {value}'


# if __name__ == '__main__':
#     app.run_server(debug=True)

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

app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("AgeEst, an age estimation web app"),
        html.Hr(),
        dbc.DropdownMenu(
            label="Select input variable set",
            menu_variant="dark",
            id='select-input-variable-set',
            children=[
                dbc.DropdownMenuItem("Item 1"),
                dbc.DropdownMenuItem("Item 2"),
                dbc.DropdownMenuItem("Item 3"),
            ],
        ),
        html.Br(),
        # dbc.DropdownMenu(
        #     # label="Select input variable set",
        #     menu_variant="dark",
        #     id='input-variables',
        #     children=[]
        # ),
        dbc.RadioItems(
            id="radio",
            options=[
                {"label": "Option 1", "value": "value1"},
                {"label": "Option 2", "value": "value2"},
                {"label": "Option 3", "value": "value3"}
            ],
            value="value1",
            inline=True
        ),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Scatter", tab_id="scatter"),
                dbc.Tab(label="Histograms", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Row(
                [
                    dbc.Col(dcc.Graph(figure=data["hist_1"]), width=6),
                    dbc.Col(dcc.Graph(figure=data["hist_2"]), width=6),
                ]
            )
    return "No tab selected"


@app.callback(
    Output(component_id="store", component_property="data"),
    Input(component_id="button", component_property="n_clicks")
    )
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}

vars = {
    "Suchey Brooks 1990": [
        'Right Phase Suchey'
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
        'Right Apical changes',
        'Right Phase Suchey',
        'Right Phase',
        'Right Transverse organization',
        'Right Surface texture',
        'Right Microposity',
        'Right Macroporositty',
        'Right Apical changes',
        'Right Phase Suchey'
    ]
}




if __name__ == "__main__":
    app.run_server(debug=True)
