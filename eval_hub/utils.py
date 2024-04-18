from typing import Dict, List

import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify
from dash.development.base_component import Component
from plotly.io import from_json

from eval_hub.components import _create_delete_plot_block_modal, _create_login_modal
from eval_hub.layout import create_left_header
from eval_hub.names import IDs
from eval_hub.report_data_classes import GraphData, GraphParameters
from names import IDs


def find_add_text_block_btn(children: List[dict], search_id: Dict[str, str]) -> int:
    search_id = {'type': IDs.NEW_BLOCK_BTN_TOOLTIP, 'index': search_id['index']}
    for chl_id, d in enumerate(children):
        if d['props']['id'] == search_id:
            return chl_id
    raise ValueError(f"Could not find id {search_id} in children list")


def _create_modals():
    return [
        _create_delete_plot_block_modal(),
        _create_login_modal()
    ]


def _create_stores():
    return [
        dcc.Store(id=IDs.DELETE_PLOT_BLOCK_STORE),
        dcc.Store(id=IDs.USER_AUTH_STORE, storage_type='local'),
        dcc.Store(id=IDs.COMMENT_STORE),
        dcc.Store(id=IDs.SELECTED_PLOT_ID_STORE),
        dcc.Store(id=IDs.LATEST_BLOCK_IND)
    ]


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
                dmc.Button(id=IDs.LOGIN_BTN, children='Login', color='blue'),
            ], style={'border-right': '1px solid gray', 'height': '100vh'})

        ],
        className="sidebar",
    )


def create_params_hover_card(
        graph_parameters: GraphParameters,
):
    return dmc.HoverCard([
        dmc.HoverCardTarget([
            DashIconify(icon='jam:settings-alt', color='gray', width=20),
        ]),
        dmc.HoverCardDropdown([
            create_graph_params_text(graph_parameters)
        ]),
    ], withArrow=True, position='right', shadow='md'),


def create_plot_block(
        graph_parameters: GraphParameters,
        graph_data: GraphData,
        description: str,
        graph_block_id: str
) -> List[Component]:
    return [dmc.Group([
        create_params_hover_card(graph_parameters),
        dmc.ActionIcon(
                DashIconify(icon="mdi:comments-text", color='gray', width=30),
                size='xl',
                id={'type': IDs.COMMENT_ICON, 'index': graph_block_id}
        ),
    ], position='apart'),

    dmc.Text(description, color='gray', size='md', weight=400, align='left'),
    dcc.Graph(figure=from_json(graph_data)),
]


def create_graph_params_text(graph_parameters: GraphParameters):
    children = []
    for name, value in graph_parameters.items():
        children.extend([html.Span(f'{name}: ', style={'font-weight': 'bold'}), value, html.Br()])

    return html.P(children)
