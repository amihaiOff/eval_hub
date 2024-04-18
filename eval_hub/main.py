import flask
from dash import Dash

from eval_hub.utils import _create_modals, _create_nav_bar, _create_stores
from callbacks import *
from names import IDs


# Initialize Flask server and Dash app
server = flask.Flask(__name__)
app = Dash(__name__,
           server=server,
           external_scripts=['https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.js'],
           external_stylesheets=['https://cdn.jsdelivr.net/npm/summernote@0.8.18/dist/summernote.min.css'],
           suppress_callback_exceptions=True)


# Basic user authentication setup
def authenticate_user(username, password):
    # Placeholder for user authentication logic
    return username == "admin" and password == "admin"


def create_layout():
    return dmc.NotificationsProvider([
        dmc.Container([
            *_create_stores(),
            *_create_modals(),
            _create_nav_bar(),
            html.Div([],
                     id=IDs.PAGE_CONTENT,
                     style={'margin-left': '6rem'})
        ], fluid=True)
    ])


app.layout = create_layout


@server.route('/health')
def health():
    return "ok"


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
