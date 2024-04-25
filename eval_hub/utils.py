from typing import Dict, List

from dash import dcc, html

from eval_hub.components import _create_delete_plot_block_modal, _create_login_modal
from eval_hub.report_data_classes import GraphParameters
from names import IDs


def find_add_text_block_btn(children: List[dict], search_id: Dict[str, str]) -> int:
    search_id = {'type': IDs.NEW_BLOCK_BTN, 'index': search_id['index']}
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
        dcc.Store(id=IDs.LATEST_BLOCK_IND, storage_type='memory', data=0)
    ]


def create_graph_params_text(graph_parameters: GraphParameters):
    children = []
    for name, value in graph_parameters.items():
        children.extend([html.Span(f'{name}: ', style={'font-weight': 'bold'}), value, html.Br()])

    return html.P(children)
