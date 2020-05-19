import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import pandas as pd
import sqlite3

import plotly.graph_objs as go

# Import Dependencies and Data
conn = sqlite3.connect(r"./wine_data.sqlite")
c = conn.cursor()
df = pd.read_sql("select * from wine_data", conn)
df = df[['country', 'description', 'rating', 'price', 'province', 'title', 'variety', 'winery', 'color']]
print(df.head(1))

# Configure the Dash App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.config.suppress_callback_exceptions = True

# Add the Layout
app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Tab one', value='tab-1'),
        dcc.Tab(label='Tab two', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])


# callback to control the tab content
@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(dash_table.DataTable(
            id='table-sorting-filtering',
            columns=[
                {'name': i, 'id': i, 'deletable': True} for i in df.columns
            ],
            style_table={'overflowX': 'scroll'},
            style_cell={
                'height': '90',
                # all three widths are needed
                'minWidth': '140px', 'width': '140px', 'maxWidth': '140px',
                'whiteSpace': 'normal'
            },
            page_current=0,
            page_size=50,
            page_action='custom',
            filter_action='custom',
            filter_query='',
            sort_action='custom',
            sort_mode='multi',
            sort_by=[]
        )
        )
    elif tab == 'tab-2':
        return html.Div([
            dcc.Graph(
                id='rating-price',
                figure={
                    'data': [
                        dict(
                            y=df['price'],
                            x=df['rating'],
                            mode='markers',
                            opacity=0.7,
                            marker={
                                'size': 8,
                                'line': {'width': 0.5, 'color': 'white'}
                            },
                            name='Price v Rating'
                        )
                    ],
                    'layout': dict(
                        xaxis={'type': 'log', 'title': 'Rating'},
                        yaxis={'title': 'Price'},
                        margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                        legend={'x': 0, 'y': 1},
                        hovermode='closest'
                    )
                }
            )
        ])


if __name__ == '__main__':
    app.run_server(debug=True)

# https://medium.com/swlh/dashboards-in-python-for-beginners-and-everyone-else-using-dash-f0a045a86644