import flask
from dash import Dash, html
import dash_mantine_components as dmc

from structure import create_available_reports, create_folder_header, create_left_header, create_page_content
from callbacks import *

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


def get_report_data():
    from report_data_classes import generate_dummy_report_data
    return generate_dummy_report_data()


def create_layout():
    return dmc.NotificationsProvider([
        dmc.Container([
            _create_nav_bar(),
            dmc.Grid([
                dmc.Col([create_page_content(get_report_data())], span=11,
                        style={'margin-left': '6rem'})
            ])
        ], fluid=True)
    ])


app.layout = create_layout()


@server.route('/health')
def health():
    return "ok"


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
