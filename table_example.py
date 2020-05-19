import dash
import dash_html_components as html
import dash_core_components as dcc
from reddit import RedditData


def generate_table(dataframe, max_rows=10):
    return html.Table(children=[
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

rd = RedditData()
app.layout = html.Div(children=[
    html.Label('Dropdown'),
    dcc.Dropdown(
        id='subreddit_dropdown',
        options=[
            {'label': 'The Netherlands', 'value': 'thenetherlands'},
            {'label': 'Programmer Humor', 'value': 'ProgrammerHumor'},
            {'label': 'Python', 'value': 'Python'}
        ],
        value='thenetherlands'
    ),

    html.H4(id='selected_subreddit', children='nothing selected'),
    generate_table(rd.rd_df('thenetherlands'))
])


@app.callback(
    dash.dependencies.Output('selected_subreddit', 'children'),
    [dash.dependencies.Input('subreddit_dropdown', 'value')])
def update_output(value):
    rd.rd_df(value)
    return f'Last from {value}'


if __name__ == '__main__':
    app.run_server(debug=True)
