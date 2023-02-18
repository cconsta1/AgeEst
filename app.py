"""
 @file app.py
 A web app for deploying age estimation machine learning
 models
 
 Language: Python (Dash)
 
 Chrysovalantis Constantinou
 
 The Cyprus Institute
 
 + 11/01/22 (cc): Created.
 + 01/25/23 (cc): Basic functional version completed
 + 02/15/23 (cc): Remove tensorflow 
"""

import time
import dash
import dash_bootstrap_components as dbc
import pickle
import numpy as np
import plotly.graph_objs as go
from dash import Input, Output, State, dcc, html
# import tensorflow as tf
# from tensorflow import keras
# from keras.models import load_model
#import xgboost
import re


app = dash.Dash(external_stylesheets=[
                dbc.themes.COSMO])

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

row_1 = dbc.Row(
    [
        dbc.Label("Phase BS",),
        dbc.Input(id="row_1_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_1_button', n_clicks=0, ),
    ],
    #style={'visibility': 'hidden'},
    id="row_1"
)

row_2 = dbc.Row(
    [
        dbc.Label("1-midlamdoid",),
        dbc.Input(id="row_2_Right_1-midlamdoid",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("2-lambda",),
        dbc.Input(id="row_2_2-lambda",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("3-obelion",),
        dbc.Input(id="row_2_3-obelion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("4-anterior sagital",),
        dbc.Input(id="row_2_4-anterior_sagital",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("5-bregma",),
        dbc.Input(id="row_2_5-bregma",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("6-midcoronal",),
        dbc.Input(id="row_2_Right_6-midcoronal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("7-pterion",),
        dbc.Input(id="row_2_Right_7-pterion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("8-sphenofrontal",),
        dbc.Input(id="row_2_Right_8-sphenofrontal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("9-inferior sphenotemporal",),
        dbc.Input(id="row_2_Right_9-inferior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("10-superior sphenotemporal",),
        dbc.Input(id="row_2_Right_10-superior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_2_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_2"
)

row_3 = dbc.Row(
    [
        dbc.Label("Phase L",),
        dbc.Input(id="row_3_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_3_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_3"
)


row_4 = dbc.Row(
    [
        dbc.Label("Transverse organization",),
        dbc.Input(id="row_4_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Surface texture",),
        dbc.Input(id="row_4_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Microposity",),
        dbc.Input(id="row_4_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Macroporositty",),
        dbc.Input(id="row_4_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Apical changes",),
        dbc.Input(id="row_4_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_4_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_4"
)


row_5 = dbc.Row(
    [
        dbc.Label("Phase BS",),
        dbc.Input(id="row_5_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Label("Phase L",),
        dbc.Input(id="row_5_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_5_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_5"
)

row_6 = dbc.Row(
    [
        dbc.Label("Transverse organization",),
        dbc.Input(id="row_6_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Surface texture",),
        dbc.Input(id="row_6_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Microposity",),
        dbc.Input(id="row_6_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Macroporositty",),
        dbc.Input(id="row_6_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Apical changes",),
        dbc.Input(id="row_6_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Phase BS",),
        dbc.Input(id="row_6_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_6_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_6"
)

row_7 = dbc.Row(
    [
        dbc.Label("Phase BS",),
        dbc.Input(id="row_7_Right_Phase_Suchey",
                  type="number", min=1, max=6, step=1, ),
        dbc.Label("1-midlamdoid",),
        dbc.Input(id="row_7_Right_1-midlamdoid",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("2-lambda",),
        dbc.Input(id="row_7_2-lambda",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("3-obelion",),
        dbc.Input(id="row_7_3-obelion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("4-anterior sagital",),
        dbc.Input(id="row_7_4-anterior_sagital",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("5-bregma",),
        dbc.Input(id="row_7_5-bregma",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("6-midcoronal",),
        dbc.Input(id="row_7_Right_6-midcoronal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("7-pterion",),
        dbc.Input(id="row_7_Right_7-pterion",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("8-sphenofrontal",),
        dbc.Input(id="row_7_Right_8-sphenofrontal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("9-inferior sphenotemporal",),
        dbc.Input(id="row_7_Right_9-inferior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("10-superior sphenotemporal",),
        dbc.Input(id="row_7_Right_10-superior_sphenotemporal",
                  type="number", min=0, max=3, step=1, ),
        dbc.Label("Phase L",),
        dbc.Input(id="row_7_Right_Phase",
                  type="number", min=1, max=8, step=1, ),
        dbc.Label("Transverse organization",),
        dbc.Input(id="row_7_Right_Transverse_organization",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Surface texture",),
        dbc.Input(id="row_7_Right_Surface_texture",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Microposity",),
        dbc.Input(id="row_7_Right_Microposity",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Macroporositty",),
        dbc.Input(id="row_7_Right_Macroporositty",
                  type="number", min=1, max=5, step=1, ),
        dbc.Label("Apical changes",),
        dbc.Input(id="row_7_Right_Apical_changes",
                  type="number", min=1, max=5, step=1, ),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Button('Submit', id='row_7_button', n_clicks=0, )
    ],
    # style={'visibility': 'hidden'},
    id="row_7"
)

SIDEBAR_STYLE = {
    "position": "absolute",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "height": "126rem",
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

sidebar = html.Div(
    [
        html.H2("Input", className="display-4"),
        html.Hr(),
        html.P(
            "Select skeletal age-at-death estimation method", className="lead"
        ),
        dbc.Nav(
            [
                dbc.Accordion([
                    dbc.AccordionItem(
                        [
                            row_1
                        ],
                        title="Brooks & Suchey 1990 (BS)",
                    ),
                    dbc.AccordionItem(
                        [
                            row_2
                        ],
                        title="Meindl and Lovejoy 1985 (ML)",
                    ),
                    dbc.AccordionItem(
                        [
                            row_3
                        ],
                        title="Lovejoy et al. 1995 (L)",
                    ),
                    dbc.AccordionItem(
                        [
                            row_4
                        ],
                        title="Buckberry & Chamberlain 2002 (BC)",
                    ),
                    dbc.AccordionItem(
                        [
                            row_5
                        ],
                        title="BS & L",
                    ),
                    dbc.AccordionItem(
                        [
                            row_6
                        ],
                        title="BS & BC",
                    ),
                    dbc.AccordionItem(
                        [
                            row_7
                        ],
                        title="BS & ML & L & BC",
                    )
                ],
                start_collapsed=True,
                flush=True
                ),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    style=CONTENT_STYLE,
    children=[
        html.H1('Output'),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Row(id="page-content"),
        html.Hr(style={'visibility': 'hidden','clear': 'both'}),
        dbc.Row(id="ann-models")
    ]
)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(
    [Output("page-content", "children"), Output("ann-models", "children")],
    [
        Input("row_1_button", "n_clicks"),
        Input("row_2_button", "n_clicks"),
        Input("row_3_button", "n_clicks"),
        Input("row_4_button", "n_clicks"),
        Input("row_5_button", "n_clicks"),
        Input("row_6_button", "n_clicks"),
        Input("row_7_button", "n_clicks")
    ],
    [
        State("row_1_Right_Phase_Suchey", "value"),
        State("row_2_Right_1-midlamdoid", "value"),
        State("row_2_2-lambda", "value"),
        State("row_2_3-obelion", "value"),
        State("row_2_4-anterior_sagital", "value"),
        State("row_2_5-bregma", "value"),
        State("row_2_Right_6-midcoronal", "value"),
        State("row_2_Right_7-pterion", "value"),
        State("row_2_Right_8-sphenofrontal", "value"),
        State("row_2_Right_9-inferior_sphenotemporal", "value"),
        State("row_2_Right_10-superior_sphenotemporal", "value"),
        State("row_3_Right_Phase", "value"),
        State("row_4_Right_Transverse_organization", "value"),
        State("row_4_Right_Surface_texture", "value"),
        State("row_4_Right_Microposity", "value"),
        State("row_4_Right_Macroporositty", "value"),
        State("row_4_Right_Apical_changes", "value"),
        State("row_5_Right_Phase_Suchey", "value"),
        State("row_5_Right_Phase", "value"),
        State("row_6_Right_Transverse_organization", "value"),
        State("row_6_Right_Surface_texture", "value"),
        State("row_6_Right_Microposity", "value"),
        State("row_6_Right_Macroporositty", "value"),
        State("row_6_Right_Apical_changes", "value"),
        State("row_6_Right_Phase_Suchey", "value"),
        State("row_7_Right_Phase_Suchey", "value"),
        State("row_7_Right_1-midlamdoid", "value"),
        State("row_7_2-lambda", "value"),
        State("row_7_3-obelion", "value"),
        State("row_7_4-anterior_sagital", "value"),
        State("row_7_5-bregma", "value"),
        State("row_7_Right_6-midcoronal", "value"),
        State("row_7_Right_7-pterion", "value"),
        State("row_7_Right_8-sphenofrontal", "value"),
        State("row_7_Right_9-inferior_sphenotemporal", "value"),
        State("row_7_Right_10-superior_sphenotemporal", "value"),
        State("row_7_Right_Phase", "value"),
        State("row_7_Right_Transverse_organization", "value"),
        State("row_7_Right_Surface_texture", "value"),
        State("row_7_Right_Microposity", "value"),
        State("row_7_Right_Macroporositty", "value"),
        State("row_7_Right_Apical_changes", "value"),
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

        if button_id == "row_1_button":
            X = [[input1_1]]

            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Suchey_Brooks_1990", X)

            rmse, rmse_tf = regression_model_info_extractor("Suchey_Brooks_1990")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)

            return classification, regression

        
        if button_id == "row_2_button":
            X = [[input2_1, input2_2, input2_3, input2_4, input2_5, \
                  input2_6, input2_7, input2_8, input2_9, input2_10]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Meindl_and_Lovejoy", X)

            rmse, rmse_tf = regression_model_info_extractor("Meindl_and_Lovejoy")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression
            
        if button_id == "row_3_button":
            X = [[input3_1]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Lovejoy_et_al", X)
            
            rmse, rmse_tf = regression_model_info_extractor("Lovejoy_et_al")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression

        if button_id == "row_4_button":
            X = [[input4_1, input4_2, input4_3, input4_4, input4_5]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Buckberry_and_Chamberlain", X)

            rmse, rmse_tf = regression_model_info_extractor("Buckberry_and_Chamberlain")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression
            
          
        if button_id == "row_5_button":
            X = [[input5_1, input5_2]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Suchey_Brooks_1990_and_Lovejoy_et_al", X)

            rmse, rmse_tf = regression_model_info_extractor("Suchey_Brooks_1990_and_Lovejoy_et_al")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression
   
            
        if button_id == "row_6_button":
            X = [[input6_1, input6_2, input6_3, input6_4, input6_5, input6_6]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("Suchey_Brooks_1990_and_Buckberry_Chamberlain", X)
            
            rmse, rmse_tf = regression_model_info_extractor("Suchey_Brooks_1990_and_Buckberry_Chamberlain")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression
            


        if button_id == "row_7_button":
            X = [[input7_1, input7_2, input7_3, input7_4, input7_5, input7_6, input7_7, \
                    input7_8, input7_9, input7_10, input7_11, input7_12, input7_13, \
                    input7_14, input7_15, input7_16, input7_17]]
            
            y_classification_sklearn, y_classification_tf, y_regression_sklearn, \
            y_regression_tf, y_proba_sklearn, y_proba_tf = calculate_y_vectors("All", X)
            
            rmse, rmse_tf = regression_model_info_extractor("All")
            
            regression = output_regression(y_regression_sklearn[0],rmse,y_regression_tf[0],rmse_tf)

            classification = output_classification(y_classification_sklearn[0], \
                                                   y_classification_tf[0], y_proba_sklearn, y_proba_tf)
            
            return classification, regression

    return "Welcome to AgeEst, a skeletal age-at-death estimation tool", "Please enter your selection on the sidebar to get started"


def output_classification(y_sklearn, y_tf, y_proba_sklearn, y_proba_tf):

    text = (
        f"The sample was divided into three age groups: "
        f"14-34 (class 0), 35-49 (class 1), and 50+ (class 2). "
        f"Utilizing classification algorithms from the sklearn library we predict "
        f"that the given input belongs to class {y_sklearn}, "
        f"with the following probabilities for each class: {y_proba_sklearn[0][0]*100:.2f}% for class 0, "
        f"{y_proba_sklearn[0][1]*100:.2f}% for class 1, and {y_proba_sklearn[0][2]*100:.2f}% for class 2. "
        f"Additionally, using a neural network from the sklearn library, we predict that the input "
        f"belongs to class {y_tf}, "
        f"with the following probabilities for each class: {y_proba_tf[0][0]*100:.2f}% for class 0, "
        f"{y_proba_tf[0][1]*100:.2f}% for class 1, and {y_proba_tf[0][2]*100:.2f}% for class 2."
    )

    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Classification", className="card-title"),
                html.P(
                    text
                ),
            ]
        ),
        style={"width": "48rem"},
    )

    return card



def output_regression(result_sklearn, rmse_sklearn, result_tf, rmse_tf):

    text = (
        f"We can make a direct prediction for age using regression. "
        f"With the help of regression algorithms from the sklearn library, we predict an age of {result_sklearn:.1f}"
        f"\u00B1"
        f"{rmse_sklearn:.1f}"
        f". "
        f"Additionally, our neural network predicts an age of {result_tf:.1f}"
        f"\u00B1"
        f"{rmse_tf:.1f}"
    )

    card = dbc.Card(
        dbc.CardBody(
            [
                html.H5("Regression", className="card-title"),
                html.P(
                    text
                ),
            ]
        ),
        style={"width": "48rem"},
    )

    return card



def calculate_y_vectors(model, X):
    classification_model_sklearn =  \
        pickle.load(
            open("".join(["./models/classification_right_",model,".dat"]), "rb"))
    classification_model_tf = \
        pickle.load(
            open("".join(["./models/ann_classification_right_",model,".dat"]), "rb"))
        
        
    # load_model(
    #         "".join(["./models/ann_classification_right_",model,".h5"]))

    regression_model_sklearn = \
        pickle.load(
            open("".join(["./models/regression_right_",model,".dat"]), "rb"))
    regression_model_tf = \
        pickle.load(
            open("".join(["./models/ann_regression_right_",model,".dat"]), "rb"))
        # load_model(
        #     "".join(["./models/ann_regression_right_",model,".h5"]))

    y_classification_sklearn = classification_model_sklearn.predict(X)

    y_proba_sklearn = classification_model_sklearn.predict_proba(X)

    

    y_classification_tf = classification_model_tf.predict(X)

    y_proba_tf = classification_model_tf.predict_proba(X)

     
    #y_classification_tf = np.argmax(y_classification_tf, axis=1)

    y_regression_sklearn = regression_model_sklearn.predict(X)
    y_regression_tf = regression_model_tf.predict(X)

    return y_classification_sklearn, y_classification_tf, \
        y_regression_sklearn, y_regression_tf, \
        y_proba_sklearn, y_proba_tf



def regression_model_info_extractor(variable_set):

    skelearn_file = "".join(["./models/regression_right_",variable_set,".txt"])

    tf_file = "".join(["./models/ann_regression_right_",variable_set,".txt"])

    #print(skelearn_file)

    best_classifier = ""
    r2_test, r2_train, rmse, mae = 0.0, 0.0, 0.0, 0.0

    rmse_tf = 0.0

    with open(skelearn_file, 'r') as f:

        contents = f.read()
        lines = contents.split("\n")
        

        for line in lines:
            if re.search("Best classifier", line):
                pattern = r"learner': (.*?)\("
                match = re.search(pattern, line)

                if match:
                    extracted_text = match.group(1)
                    best_classifier = extracted_text
                    #print(best_classifier)
                # else:
                #     #print("No match found")

            if re.search("(test)", line):
                matches = re.findall(r"\d+\.\d+", line)
                numbers = [float(match) for match in matches]
                r2_test, r2_train = numbers
                #print(r2_test, r2_train)

            if re.search("RMSE", line):
                matches = re.findall(r"\d+\.\d+", line)
                numbers = [float(match) for match in matches]
                rmse = numbers[0]
                #print(rmse)

            if re.search("MAE", line):
                matches = re.findall(r"\d+\.\d+", line)
                numbers = [float(match) for match in matches]
                mae = numbers[0]
                #print(mae)

    with open(tf_file, 'r') as f:
        contents = f.read()
        lines = contents.split("\n")

        for line in lines:
            if re.search("RMSE", line):
                matches = re.findall(r"\d+\.\d+", line)
                numbers = [float(match) for match in matches]
                rmse_tf = numbers[0]
                #print(rmse_tf)
    
    return rmse, rmse_tf


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0",port="8050", use_reloader=True)
    #app.run_server(debug=True)