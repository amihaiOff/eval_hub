import uuid
from datetime import datetime

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

from names import IDs
from layout import create_comment, Comment


@dash.callback(
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
    return patched_children


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
    Input()
)
def update_page(report_name):
    report_name = 'report1'
