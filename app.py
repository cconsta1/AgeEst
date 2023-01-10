# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import plotly.express as px
import pandas as pd
import pickle
import numpy as np

app = Dash(__name__)
server = app.server

test_model = pickle.load(open("./left_women_Meindl_and_Lovejoy.dat", "rb"))

print(test_model.predict(np.array([[1,2,1,1,2,1,3,1,3,1]]))[0])



app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=['''
        Dash: A web application framework for your data
    ''']),

    html.H1(children=['''
    Example calculation 
    ''', test_model.predict(np.array([[1,2,1,1,2,1,3,1,3,1]]))[0]]
    ),

    

])

if __name__ == '__main__':
    app.run_server(debug=True)


