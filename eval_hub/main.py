import flask
from dash import Dash, html, dcc, Input, Output, State
import plotly.graph_objs as go
import uuid

# Simulated database for plots and comments
plots_db = {
    uuid.uuid4().hex: {
        "title":       "Example Plot 1",
        "description": "This is an example of a Plotly plot.",
        "figure":      go.Figure(data=[go.Bar(x=[1, 2, 3], y=[3, 1, 2], name="Example Data")])
    }
}

comments_db = {
    list(plots_db.keys())[0]: ["First comment!"]
}

# Initialize Flask server and Dash app
server = flask.Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)


# Basic user authentication setup
def authenticate_user(username, password):
    # Placeholder for user authentication logic
    return username == "admin" and password == "admin"


# App layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='user-authentication-section'),
    html.Div([
        html.Div([
            html.Div(id='plot-section', children=[
                html.Div([
                    dcc.Graph(id=f'plot-{plot_id}', figure=plot_info["figure"]),
                    html.H3(plot_info["title"]),
                    html.P(plot_info["description"]),
                    html.Button('Show Comments', id={'type': 'show-comments', 'index': plot_id}, n_clicks=0),
                ], style={'border': '1px solid black', 'padding': '10px', 'margin': '10px'})
                for plot_id, plot_info in plots_db.items()
            ]),
        ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top'}),
        html.Div([
            html.Div(id='comments-section')
        ], style={'width': '35%', 'display': 'inline-block', 'marginLeft': '5%'}),
    ]),
])


# Callback for user authentication
@app.callback(
        Output('user-authentication-section', 'children'),
        [Input('url', 'pathname')]
)
def display_page(pathname):
    # Simulate user login page
    return html.Div([
        html.H2('User Login'),
        dcc.Input(placeholder='Username', type='text', id='username'),
        dcc.Input(placeholder='Password', type='password', id='password'),
        html.Button('Login', id='login-button'),
        html.Div(id='login-status')
    ])


# Callback to update the comments section
@app.callback(
        Output('comments-section', 'children'),
        [Input({'type': 'show-comments', 'index': ALL}, 'n_clicks')],
        [State({'type': 'show-comments', 'index': ALL}, 'id')],
        prevent_initial_call=True
)
def update_comments(n_clicks, ids):
    if not any(n_clicks):
        return "Select a plot to see comments."

    # Find which button was clicked
    button_id = [id['index'] for n, id in zip(n_clicks, ids) if n > 0][0]

    # Fetch comments for the selected plot
    comments = comments_db.get(button_id, [])

    return html.Div([
        html.Ul([html.Li(comment) for comment in comments]),
        dcc.Textarea(id='new-comment', style={'width': '100%', 'height': '100px'}),
        html.Button('Submit Comment', id='submit-comment', n_clicks=0,
                    n_clicks_timestamp=0,
                    style={'display': 'block', 'margin': 'auto'}),
        html.Div(id={'type': 'comment-submission-status', 'index': button_id})
    ])


# Callback for comment submission
@app.callback(
        Output({'type': 'comment-submission-status', 'index': MATCH}, 'children'),
        [Input('submit-comment', 'n_clicks')],
        [State('new-comment', 'value'), State({'type': 'show-comments', 'index': MATCH}, 'id')],
        prevent_initial_call=True
)
def submit_comment(n_clicks, comment, id):
    if comment:
        plot_id = id['index']
        comments_db.setdefault(plot_id, []).append(comment)
        return "Comment submitted!"
    return "Please enter a comment."


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
