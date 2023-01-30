"""
 @file app.py
 A web app for deploying age estimation machine learning
 models
 
 Language: Python (Dash)
 
 Chrysovalantis Constantinou
 
 The Cyprus Institute
 
 + 11/01/22 (cc): Created.
 + 01/25/23 (cc): Basic functional version completed
"""

import time
import dash
import dash_bootstrap_components as dbc
import pickle
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import xgboost




app = dash.Dash(external_stylesheets=[
                dbc.themes.BOOTSTRAP])

app.title = "AgeEst"

# Include the server option to become able to deploy online
server = app.server

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

# print("_".join(["hidden_row_1", "Right Phase Suchey".replace(" ", "_")]))

hidden_row_1 = dbc.Row(
    [
        dbc.Label("Right Phase Suchey",),
        dbc.Input(id="hidden_row_1_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Button('Submit', id='hidden_row_1_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_1"
)

hidden_row_2 = dbc.Row(
    [
        dbc.Label("Right 1-midlamdoid",),
        dbc.Input(id="hidden_row_2_Right_1-midlamdoid",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("2-lambda",),
        dbc.Input(id="hidden_row_2_2-lambda",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("3-obelion",),
        dbc.Input(id="hidden_row_2_3-obelion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("4-anterior sagital",),
        dbc.Input(id="hidden_row_2_4-anterior_sagital",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("5-bregma",),
        dbc.Input(id="hidden_row_2_5-bregma",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 6-midcoronal",),
        dbc.Input(id="hidden_row_2_Right_6-midcoronal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 7-pterion",),
        dbc.Input(id="hidden_row_2_Right_7-pterion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 8-sphenofrontal",),
        dbc.Input(id="hidden_row_2_Right_8-sphenofrontal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 9-inferior sphenotemporal",),
        dbc.Input(id="hidden_row_2_Right_9-inferior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 10-superior sphenotemporal",),
        dbc.Input(id="hidden_row_2_Right_10-superior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Button('Submit', id='hidden_row_2_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_2"
)

hidden_row_3 = dbc.Row(
    [
        dbc.Label("Right Phase",),
        dbc.Input(id="hidden_row_3_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        dbc.Button('Submit', id='hidden_row_3_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_3"
)

hidden_row_4 = dbc.Row(
    [
        dbc.Label("Right Transverse organization",),
        dbc.Input(id="hidden_row_4_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Surface texture",),
        dbc.Input(id="hidden_row_4_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Microposity",),
        dbc.Input(id="hidden_row_4_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Macroporositty",),
        dbc.Input(id="hidden_row_4_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Apical changes",),
        dbc.Input(id="hidden_row_4_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        dbc.Button('Submit', id='hidden_row_4_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_4"
)

hidden_row_5 = dbc.Row(
    [
        dbc.Label("Right Phase Suchey",),
        dbc.Input(id="hidden_row_5_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Label("Right Phase",),
        dbc.Input(id="hidden_row_5_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        dbc.Button('Submit', id='hidden_row_5_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_5"
)

hidden_row_6 = dbc.Row(
    [
        dbc.Label("Right Transverse organization",),
        dbc.Input(id="hidden_row_6_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Surface texture",),
        dbc.Input(id="hidden_row_6_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Microposity",),
        dbc.Input(id="hidden_row_6_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Macroporositty",),
        dbc.Input(id="hidden_row_6_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Apical changes",),
        dbc.Input(id="hidden_row_6_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Phase Suchey",),
        dbc.Input(id="hidden_row_6_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Button('Submit', id='hidden_row_6_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_6"
)

hidden_row_7 = dbc.Row(
    [
        dbc.Label("Right Phase Suchey",),
        dbc.Input(id="hidden_row_7_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Label("Right 1-midlamdoid",),
        dbc.Input(id="hidden_row_7_Right_1-midlamdoid",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("2-lambda",),
        dbc.Input(id="hidden_row_7_2-lambda",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("3-obelion",),
        dbc.Input(id="hidden_row_7_3-obelion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("4-anterior sagital",),
        dbc.Input(id="hidden_row_7_4-anterior_sagital",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("5-bregma",),
        dbc.Input(id="hidden_row_7_5-bregma",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 6-midcoronal",),
        dbc.Input(id="hidden_row_7_Right_6-midcoronal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 7-pterion",),
        dbc.Input(id="hidden_row_7_Right_7-pterion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 8-sphenofrontal",),
        dbc.Input(id="hidden_row_7_Right_8-sphenofrontal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 9-inferior sphenotemporal",),
        dbc.Input(id="hidden_row_7_Right_9-inferior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right 10-superior sphenotemporal",),
        dbc.Input(id="hidden_row_7_Right_10-superior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Right Phase",),
        dbc.Input(id="hidden_row_7_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        dbc.Label("Right Transverse organization",),
        dbc.Input(id="hidden_row_7_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Surface texture",),
        dbc.Input(id="hidden_row_7_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Microposity",),
        dbc.Input(id="hidden_row_7_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Macroporositty",),
        dbc.Input(id="hidden_row_7_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Right Apical changes",),
        dbc.Input(id="hidden_row_7_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        dbc.Button('Submit', id='hidden_row_7_button', n_clicks=0, )
    ],
    style={'visibility': 'hidden'},
    id="hidden_row_7"
)

# variables_ranges = {
#     'Right Phase Suchey': [1, 6],
#     'Right 1-midlamdoid': [0, 3],
#     '2-lambda': [0, 3],
#     '3-obelion': [0, 3],
#     '4-anterior sagital': [0, 3],
#     '5-bregma': [0, 3],
#     'Right 6-midcoronal': [0, 3],
#     'Right 7-pterion': [0, 3],
#     'Right 8-sphenofrontal': [0, 3],
#     'Right 9-inferior sphenotemporal': [0, 3],
#     'Right 10-superior sphenotemporal': [0, 3],
#     "Right Phase": [1, 8],
#     'Right Transverse organization': [1, 5],
#     'Right Surface texture': [1, 5],
#     'Right Microposity': [1, 5],
#     'Right Macroporositty': [1, 5],
#     'Right Apical changes': [1, 5]
# }

SIDEBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "height": "100rem",
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
    "overflow": "hidden"
}

CONTENT_STYLE = {
    "position": "fixed",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

dropdown_items = [
    dbc.DropdownMenuItem(item, id=str(item)) for item in list(set_of_variables.keys())
]

sidebar = html.Div(
    [
        html.H2("Input", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar where users can choose what they want to do", className="lead"
        ),
        dbc.Nav(
            [
                dbc.DropdownMenu(
                    label="Select an input variable set",
                    menu_variant="dark",
                    id='input-variable-set',
                    children=dropdown_items,
                    align_end=False
                ),
            ],
            vertical=True,
            pills=True,
        ),
        dbc.Row(id='output-selected-variable-set'),
        dcc.Store(id='memory'),
        dcc.Store(id="input-variables"),
        dbc.Container(id='rows_container', 
                      children=[
                    hidden_row_1, hidden_row_2, hidden_row_3,hidden_row_4, hidden_row_5, hidden_row_6, hidden_row_7
                    ])
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    style=CONTENT_STYLE,
    children=[
        html.H1('Hello Dash'),
        dbc.Row(id="page-content"),
        dbc.Row(id="ann-models")
    ]
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(
    [
        Output("hidden_row_1", "style"),
        Output("hidden_row_2", "style"),
        Output("hidden_row_3", "style"),
        Output("hidden_row_4", "style"),
        Output("hidden_row_5", "style"),
        Output("hidden_row_6", "style"),
        Output("hidden_row_7", "style")
    ],
    [Input(str(item), 'n_clicks') for item in list(set_of_variables.keys())]
)
def toggle_visibility(*args):
    ctx = dash.callback_context

    if not ctx.triggered:
        button_id = ""
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]


    if button_id == "Suchey Brooks 1990":
        return [{'visibility': 'visible', 'position': 'relative'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'}]
    if button_id == "Meindl and Lovejoy":
        return [{'visibility': 'hidden'}, {'visibility': 'visible', 'position': 'relative', 'top': '-100px'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'}]
    if button_id == "Lovejoy et al":
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'visible', 'position': 'relative', 'top': '-884px'}, {'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'}]
    if button_id == "Buckberry and Chamberlain":
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'visible', 'position': 'relative', 'top': '-990px'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'}]
    if button_id=="Suchey Brooks 1990 and Lovejoy et al":
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'visible', 'position': 'relative', 'top': '-1390px'},{'visibility': 'hidden'},{'visibility': 'hidden'}]
    if button_id == "Suchey Brooks 1990 and Buckberry Chamberlain":
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'hidden'}, {'visibility': 'visible', 'position': 'relative', 'top': '-1575px'},{'visibility': 'hidden'}]
    if button_id=="All":
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'visible', 'position': 'relative', 'top': '-2050px'}]
    else:
        return [{'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'}, {'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'},{'visibility': 'hidden'}]


@app.callback(
    [Output("page-content", "children"), Output("ann-models", "children")],
    [
        Input("hidden_row_1_button", "n_clicks"),
        Input("hidden_row_2_button", "n_clicks"),
        Input("hidden_row_3_button", "n_clicks"),
        Input("hidden_row_4_button", "n_clicks"),
        Input("hidden_row_5_button", "n_clicks"),
        Input("hidden_row_6_button", "n_clicks"),
        Input("hidden_row_7_button", "n_clicks")
    ],
    [
        State("hidden_row_1_Right_Phase_Suchey", "value"),
        State("hidden_row_2_Right_1-midlamdoid", "value"),
        State("hidden_row_2_2-lambda", "value"),
        State("hidden_row_2_3-obelion", "value"),
        State("hidden_row_2_4-anterior_sagital", "value"),
        State("hidden_row_2_5-bregma", "value"),
        State("hidden_row_2_Right_6-midcoronal", "value"),
        State("hidden_row_2_Right_7-pterion", "value"),
        State("hidden_row_2_Right_8-sphenofrontal", "value"),
        State("hidden_row_2_Right_9-inferior_sphenotemporal", "value"),
        State("hidden_row_2_Right_10-superior_sphenotemporal", "value"),
        State("hidden_row_3_Right_Phase", "value"),
        State("hidden_row_4_Right_Transverse_organization", "value"),
        State("hidden_row_4_Right_Surface_texture", "value"),
        State("hidden_row_4_Right_Microposity", "value"),
        State("hidden_row_4_Right_Macroporositty", "value"),
        State("hidden_row_4_Right_Apical_changes", "value"),
        State("hidden_row_5_Right_Phase_Suchey", "value"),
        State("hidden_row_5_Right_Phase", "value"),
        State("hidden_row_6_Right_Transverse_organization", "value"),
        State("hidden_row_6_Right_Surface_texture", "value"),
        State("hidden_row_6_Right_Microposity", "value"),
        State("hidden_row_6_Right_Macroporositty", "value"),
        State("hidden_row_6_Right_Apical_changes", "value"),
        State("hidden_row_6_Right_Phase_Suchey", "value"),
        State("hidden_row_7_Right_Phase_Suchey", "value"),
        State("hidden_row_7_Right_1-midlamdoid", "value"),
        State("hidden_row_7_2-lambda", "value"),
        State("hidden_row_7_3-obelion", "value"),
        State("hidden_row_7_4-anterior_sagital", "value"),
        State("hidden_row_7_5-bregma", "value"),
        State("hidden_row_7_Right_6-midcoronal", "value"),
        State("hidden_row_7_Right_7-pterion", "value"),
        State("hidden_row_7_Right_8-sphenofrontal", "value"),
        State("hidden_row_7_Right_9-inferior_sphenotemporal", "value"),
        State("hidden_row_7_Right_10-superior_sphenotemporal", "value"),
        State("hidden_row_7_Right_Phase", "value"),
        State("hidden_row_7_Right_Transverse_organization", "value"),
        State("hidden_row_7_Right_Surface_texture", "value"),
        State("hidden_row_7_Right_Microposity", "value"),
        State("hidden_row_7_Right_Macroporositty", "value"),
        State("hidden_row_7_Right_Apical_changes", "value"),
    ],
)
def process_input(n_clicks1, n_clicks2, n_clicks3, n_clicks4, n_clicks5, n_clicks6, n_clicks7,
                  input1_1, 
                  input2_1, input2_2, input2_3, input2_4, input2_5, input2_6, \
                    input2_7, input2_8, input2_9, input2_10,
                  input3_1,
                  input4_1, input4_2, input4_3, input4_4, input4_5,
                  input5_1, input5_2,
                  input6_1, input6_2, input6_3, input6_4, input6_5, input6_6,
                  input7_1, input7_2, input7_3, input7_4, input7_5, input7_6, input7_7, \
                    input7_8, input7_9, input7_10, input7_11, input7_12, input7_13, \
                    input7_14, input7_15, input7_16, input7_17):
    
    ctx = dash.callback_context
    
    if ctx.triggered:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if button_id == "hidden_row_1_button":
            X = [[input1_1]]

            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Suchey_Brooks_1990", X)

            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"
        
        if button_id == "hidden_row_2_button":
            X = [[input2_1, input2_2, input2_3, input2_4, input2_5, \
                  input2_6, input2_7, input2_8, input2_9, input2_10]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Meindl_and_Lovejoy", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"



            
        if button_id == "hidden_row_3_button":
            X = [[input3_1]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Lovejoy_et_al", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"


        if button_id == "hidden_row_4_button":
            X = [[input4_1, input4_2, input4_3, input4_4, input4_5]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Buckberry_and_Chamberlain", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"
        
            
        if button_id == "hidden_row_5_button":
            X = [[input5_1, input5_2]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Suchey_Brooks_1990_and_Lovejoy_et_al", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"

        if button_id == "hidden_row_6_button":
            X = [[input6_1, input6_2, input6_3, input6_4, input6_5, input6_6]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("Suchey_Brooks_1990_and_Buckberry_Chamberlain", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"

        if button_id == "hidden_row_7_button":
            X = [[input7_1, input7_2, input7_3, input7_4, input7_5, input7_6, input7_7, \
                    input7_8, input7_9, input7_10, input7_11, input7_12, input7_13, \
                    input7_14, input7_15, input7_16, input7_17]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf = calculate_y_vectors("All", X)
            
            return f"The predicted result from sklearn (classification) is {y_classification_sklearn} \
                and from tensorflow is {y_classification_tf}", \
                    f"The predicted result from sklearn (regression) is {y_regression_sklearn} \
                and from tensorflow is {y_regression_tf}"


    return "Nothing was submitted", ""


# @app.callback(
#     Output('memory', 'data'),
#     [Input(str(item), 'n_clicks') for item in list(set_of_variables.keys())]
# )
# def save_id_to_memory(*args):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         button_id = ""
#     else:
#         button_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     if button_id in list(set_of_variables.keys()):

#         list_of_variables = [
#             item for item in list(set_of_variables[str(button_id)])
#         ]

#         list_of_variables.insert(0, button_id)

#         return list_of_variables
#     else:
#         return ''


# @app.callback(Output('users-input', 'children'),
#             # Input('output-selected-variable-set', 'children'),
#             [Input(str(item), 'value') for item in list(set_of_variables["All"])])
# def print_output(children):
#     print("888")
#     print(set_of_variables["All"])
#     return children


# @app.callback(
#     Output('output-selected-variable-set', 'children'),
#     [Input(str(item), 'n_clicks') for item in list(set_of_variables.keys())]
# )
# def update_form(*args):
#     ctx = dash.callback_context

#     if not ctx.triggered:
#         button_id = ""
#     else:
#         button_id = ctx.triggered[0]["prop_id"].split(".")[0]

#     # print(button_id)

#     if button_id in list(set_of_variables.keys()):

#         element = dbc.Row([
#             dbc.Label(item) for item in list(set_of_variables[str(button_id)])
#         ])

#         element_to_insert_with_id = [
#             dbc.Input(id=item, type="number", min=variables_ranges[item][0], max=variables_ranges[item][1], step=1) for item in list(set_of_variables[str(button_id)])]

#         for i in range(len(element.children)):
#             # print(i)
#             element.children.insert(2*i+1, element_to_insert_with_id[i])

#         element.children.append(dbc.Button('Submit', id='button', n_clicks=0))

#         # print(element)

#         return element
#     else:
#         return ''


# @app.callback(
#     Output('page-content', 'children'),
#     Input('memory', 'data')
# )
# def test_memory(data):

#     # print("\n".join(data))

#     # print(data)

#     return "-".join(data)


# @app.callback(Output("users-input", "children"),
#               [State(str(variable), "value")
#                for variable in list(set_of_variables['All'])]
#               )
# def output_text(*args):

#     ctx = dash.callback_context

#     print(ctx)

#     return 'value'

def calculate_y_vectors(model, X):
    classification_model_sklearn =  \
        pickle.load(
            open("".join(["./models/classification_right_",model,".dat"]), "rb"))
    classification_model_tf = \
        load_model(
            "".join(["./models/ann_classification_right_",model,".h5"]))

    regression_model_sklearn = \
        pickle.load(
            open("".join(["./models/regression_right_",model,".dat"]), "rb"))
    regression_model_tf = \
        load_model(
            "".join(["./models/ann_regression_right_",model,".h5"]))

    y_classification_sklearn = classification_model_sklearn.predict(X)

    y_classification_tf = classification_model_tf.predict(X)
    y_classification_tf = np.argmax(y_classification_tf, axis=1)

    y_regression_sklearn = regression_model_sklearn.predict(X)
    y_regression_tf = regression_model_tf.predict(X)

    return y_classification_sklearn, y_classification_tf, \
        y_regression_sklearn, y_regression_tf



def generate_text(input_text):
    return "malakia"


if __name__ == "__main__":
    app.run_server(debug=True)
