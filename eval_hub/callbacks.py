import uuid
from datetime import datetime
from typing import List, Union

import dash
from dash import (
    Output,
    Input,
    State,
    html,
    ctx,
    MATCH,
    ALL,
    Patch
)
from dash.exceptions import PreventUpdate

from names import IDs
from layout import create_comment, Comment, create_page_content
from report_loader import load_report


@dash.callback(
        Output({'type': IDs.COMMENT_INPUT, 'index': MATCH}, 'value'),
        Output({'type': IDs.COMMENT_STACK, 'index': MATCH}, 'children'),
        Input({'type': IDs.COMMENT_SUBMIT, 'index': MATCH}, 'n_clicks'),
        State({'type': IDs.COMMENT_INPUT, 'index': MATCH}, 'value'),
        prevent_initial_call=True
)
def add_comment(n_clicks: int, comment_text: str):
    patched_children = Patch()
    comment = Comment(id=str(uuid.uuid4()),
                      comment_text=comment_text,
                      user='user',
                      date=str(datetime.now())
                      )
    # todo add to backend storage
    patched_children.append(create_comment(comment))
    return '', patched_children


@dash.callback(
        Output({'type': IDs.FULL_SCREEN_MODAL, 'index': MATCH}, 'opened'),
        Input({'type': IDs.PLOT_EXPAND, 'index': MATCH}, 'n_clicks'),
        State({'type': IDs.PLOT_EXPAND, 'index': MATCH}, 'opened'),
        prevent_initial_call=True
)
def close_modal(n_clicks: int, opened: bool):
    return not opened


@dash.callback(
    Output(IDs.PAGE_CONTENT, 'children'),
    Input('1', 'n_clicks'),
)
def update_page(n_clicks):
    REPORTS_PATH = '../dummy_data'
    if n_clicks is None or n_clicks % 2 == 0:
       report_name = 'report1'
    else:
       report_name = 'report2'

    return create_page_content(load_report(f'{REPORTS_PATH}/{report_name}'))


@dash.callback(
        Output(IDs.DELETE_PLOT_BLOCK_MODAL, 'opened'),
        Output(IDs.DELETE_PLOT_BLOCK_STORE, 'data'),
        Input({'type': IDs.DELETE_PLOT_BLOCK_ICON, 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
)
def delete_plot_block_icon(n_clicks: Union[int, List[int]]):
    if n_clicks is None or all(n is None for n in n_clicks):
        raise PreventUpdate
    # calculate the index of the triggered element in the element stack - this will be used by
    # the delete_plot_block_model callback to determine which element to delete
    triggered_ind = [i for i, d in enumerate(ctx.args_grouping) if d['triggered'] is True]
    return True, int(triggered_ind[0])


@dash.callback(
        Output({'type': IDs.PLOT_BLOCK, 'index': ALL}, 'style'),
        Output(IDs.DELETE_PLOT_BLOCK_MODAL, 'opened', allow_duplicate=True),
        Input(IDs.DELETE_PLOT_BLOCK_MODAL_NO, 'n_clicks'),
        Input(IDs.DELETE_PLOT_BLOCK_MODAL_YES, 'n_clicks'),
        State({'type': IDs.PLOT_BLOCK, 'index': ALL}, 'style'),
        State(IDs.DELETE_PLOT_BLOCK_STORE, 'data'),
        config_prevent_initial_callbacks=True
)
def delete_plot_block_model(no_clicks: int, yes_clicks: int, styles, elem_ind: str):
    if ctx.triggered_id == IDs.DELETE_PLOT_BLOCK_MODAL_NO:
        return styles, False
    elif ctx.triggered_id == IDs.DELETE_PLOT_BLOCK_MODAL_YES:
        styles[elem_ind]['display'] = 'none'
        return styles, False


@dash.callback(
        Output({'type': IDs.COMMENT_CARD, 'index': ALL}, 'style'),
        Input({'type': IDs.COLLAPSE_COMMENTS_ICON, 'index': ALL}, 'n_clicks'),
        State({'type': IDs.COMMENT_CARD, 'index': ALL}, 'style'),
        prevent_initial_call=True
)
def collapse_comments(n_clicks: List[int], styles: List[dict]):
    for lst in ctx.args_grouping:
        for i, d in enumerate(lst):
            if d['triggered']:
                triggered_ind = i

    print(triggered_ind)
    styles[triggered_ind]['width'] = '20%'
    return styles
