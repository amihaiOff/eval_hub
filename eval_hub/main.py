import flask
from dash import Dash, html, dcc
import dash_mantine_components as dmc

from layout import create_available_reports, create_folder_header, create_left_header
from callbacks import *
from names import IDs


# Initialize Flask server and Dash app
server = flask.Flask(__name__)
app = Dash(__name__, server=server, suppress_callback_exceptions=True)


def _create_nav_bar():
    return html.Div(
        [
            dmc.Stack([
                create_left_header(),
                dmc.Space(h=30),
                dmc.Title('Select Report', order=3),
                dmc.Select(id=IDs.CUSTOMER_DD,
                           placeholder='Select customer',
                           label='Customer',
                           searchable=True,
                           data=[
                                 {'label': 'Rappi', 'value': 'rappi'},
                                 {'label': 'Uber', 'value': 'uber'},
                           ], style={'margin-right': '20px'}),

                dmc.Select(id=IDs.PRODUCT_DD,
                           placeholder='Select product',
                           label='Product',
                           searchable=True,
                           data=[
                               {'label': 'Rappi', 'value': 'rappi'},
                               {'label': 'Uber', 'value': 'uber'},
                           ], style={'margin-right': '20px'}),
                dmc.Space(h=20),
                dmc.Select(id=IDs.FLURRY_ID_DD,
                           placeholder='Select flurry id',
                           label='Flurry ID',
                           searchable=True,
                           data=[
                               {'label': 'Rappi', 'value': 'rappi'},
                               {'label': 'Uber', 'value': 'uber'},
                           ], style={'margin-right': '20px'}),

                dmc.Button(id='1', children='change report'),
            ], style={'background': '#FBFBFA', 'border-right': '1px solid gray', 'height': '100vh'})

        ],
        className="sidebar",
    )

# Basic user authentication setup
def authenticate_user(username, password):
    # Placeholder for user authentication logic
    return username == "admin" and password == "admin"


def _create_delete_plot_block_modal():
    return dmc.Modal([
        dmc.Text('Are you sure you want to delete this plot?'),
        dmc.Space(h=20),
        dmc.Group([
            dmc.Button('Yes',
                       id=IDs.DELETE_PLOT_BLOCK_MODAL_YES,
                       color='red'),
            dmc.Button('No',
                       id=IDs.DELETE_PLOT_BLOCK_MODAL_NO,
                       color='gray')
        ], position='right')
    ],
            id=IDs.DELETE_PLOT_BLOCK_MODAL,
            title='Delete plot block',
)


def _create_modals():
    return [
        _create_delete_plot_block_modal()
    ]


def _create_stores():
    return [
        dcc.Store(id=IDs.DELETE_PLOT_BLOCK_STORE)
    ]


def create_layout():
    return dmc.NotificationsProvider([
        dmc.Container([
            *_create_stores(),
            *_create_modals(),
            _create_nav_bar(),
            html.Div([create_page_content(load_report('../dummy_data/report1'))],
                     id=IDs.PAGE_CONTENT,
                     style={'margin-left': '6rem'})
            # dmc.Grid([
            #     dmc.Col([],
            #             id=IDs.PAGE_CONTENT,
            #             span=11,
            #             style={'margin-left': '6rem'})
            # ])
        ], fluid=True)
    ])


app.layout = create_layout


@server.route('/health')
def health():
    return "ok"


# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
