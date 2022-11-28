# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import pickle
import numpy as np

app = Dash(__name__)
server = app.server



test_model = pickle.load(open("./test_pipe_model_for_dash.dat", "rb"))

print(test_model.predict(np.array([[1, 2, 2, 2, 2, 2]]))[0])

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# fig.layout.height = 5000

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children=['''
        Dash: A web application framework for your data.
    ''', "hi"]),

    html.H1(children=['''
    Yessss!!
    ''', 'hi ', test_model.predict(np.array([[1, 2, 2, 2, 2, 2]]))[0]]
    ),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)


