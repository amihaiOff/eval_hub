import flask
from dash import Dash, html, dcc, Input, Output, State
import dash_mantine_components as dmc

from eval_hub.helpers import create_user_avatar
from structure import create_available_reports, create_folder_header, create_left_header, create_left_panel, \
    create_right_panel

# Initialize Flask server and Dash app
server = flask.Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)


def _create_nav_bar():
    return html.Div(
        [
            dmc.Stack([
                create_left_header(),
                dmc.Space(h=50),
                create_folder_header(),
                create_available_reports()

            ], style={'background': '#FBFBFA', 'border-right': '1px solid gray', 'height': '100vh'})

        ],
        className="sidebar",
    )

# Basic user authentication setup
def authenticate_user(username, password):
    # Placeholder for user authentication logic
    return username == "admin" and password == "admin"


def create_layout():
    return dmc.Container([
        _create_nav_bar(),
        dmc.Grid([
            dmc.Col([create_right_panel()], span=11,
                    style={'margin-left': '6rem'})
        ])
    ], fluid=True)

app.layout = create_layout()


@server.route('/health')
def health():
    return "ok"


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
