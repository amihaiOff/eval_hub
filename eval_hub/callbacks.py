import uuid
from datetime import datetime
from typing import Dict, List, Union

import dash
import dash_mantine_components as dmc
from dash_iconify import DashIconify
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

from eval_hub.utils import find_add_text_block_btn
from eval_hub.components import create_comments_section_open_icon, create_textblock
from names import IDs
from layout import create_comment, Comment, create_page_content, create_comments_section
from report_loader import load_report


@dash.callback(
        Output(IDs.COMMENT_INPUT, 'value'),
        Output(IDs.COMMENTS_STACK, 'children'),
        Input(IDs.COMMENT_SUBMIT, 'n_clicks'),
        State(IDs.COMMENT_INPUT, 'value'),
        State(IDs.SELECTED_PLOT_ID_STORE, 'data'),
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
    Output(IDs.PAGE_CONTENT, 'children'),
    Output(IDs.COMMENT_STORE, 'data'),
    Output(IDs.SELECTED_PLOT_ID_STORE, 'data'),
    Input('1', 'n_clicks'),
)
def update_page(n_clicks):
    REPORTS_PATH = '../dummy_data'
    if n_clicks is None or n_clicks % 2 == 0:
       report_name = 'report1'
    else:
       report_name = 'report2'

    report_data = load_report(f'{REPORTS_PATH}/{report_name}')
    first_graph_block = report_data.graph_blocks[0]
    return create_page_content(report_data), \
        report_data.get_comments_as_dict(), \
        first_graph_block.id


@dash.callback(
        Output(IDs.DELETE_PLOT_BLOCK_MODAL, 'opened'),
        Output(IDs.DELETE_PLOT_BLOCK_STORE, 'data'),
        Input({'type': IDs.DELETE_BLOCK_ICON, 'index': ALL}, 'n_clicks'),
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
        Output(IDs.PLOTS_COL, 'children'),
        Output(IDs.DELETE_PLOT_BLOCK_MODAL, 'opened', allow_duplicate=True),
        Input(IDs.DELETE_PLOT_BLOCK_MODAL_NO, 'n_clicks'),
        Input(IDs.DELETE_PLOT_BLOCK_MODAL_YES, 'n_clicks'),
        State(IDs.PLOTS_COL, 'children'),
        State(IDs.DELETE_PLOT_BLOCK_STORE, 'data'),
        config_prevent_initial_callbacks=True
)
def delete_plot_block_model(no_clicks: int, yes_clicks: int, children, elem_ind: str):
    if ctx.triggered_id == IDs.DELETE_PLOT_BLOCK_MODAL_NO:
        return dash.no_update, False
    elif ctx.triggered_id == IDs.DELETE_PLOT_BLOCK_MODAL_YES:
        # todo remove from backend
        patched_children = Patch()
        patched_children.remove(children[elem_ind])
        return patched_children, False


@dash.callback(
        Output(IDs.USER_AUTH_STORE, 'data', allow_duplicate=True),
        Output(IDs.LOGIN_MODAL, 'opened', allow_duplicate=True),
        Input(IDs.LOGIN_MODAL_LOGIN, 'n_clicks'),
        State(IDs.USERNAME_INPUT, 'value'),
        prevent_initial_call=True
)
def login(n_clicks, username: str):
    # todo add checks
    return username, False


@dash.callback(
        Output(IDs.LOGIN_MODAL, 'opened'),
        Input(IDs.LOGIN_BTN, 'n_clicks'),
        State(IDs.USER_AUTH_STORE, 'data'),
)
def check_auth(n_clicks: int, user: str):
    n_clicks = n_clicks or 0  # n_clicks is None on the first call
    if user is None or n_clicks > 0:
        return True
    return False


@dash.callback(
        Output(IDs.COMMENTS_STACK, 'children', allow_duplicate=True),
        Output(IDs.COMMENTS_SECTION_TITLE, 'children', allow_duplicate=True),
        Output(IDs.SELECTED_PLOT_ID_STORE, 'data', allow_duplicate=True),
        Input({'type': IDs.COMMENT_ICON, 'index': ALL}, 'n_clicks'),
        State(IDs.COMMENT_STORE, 'data'),
        prevent_initial_call=True
)
def update_comments(n_clicks,
                    all_comments: Dict[str, List[Comment]]):
    selected_plot_id = ctx.triggered_id['index']
    comments = [Comment(**cmt) for cmt in all_comments[selected_plot_id]]
    return [create_comment(cmt) for cmt in comments], selected_plot_id, selected_plot_id


@dash.callback(
        Output(IDs.COMMENTS_COL, 'children'),
        Output(IDs.COMMENTS_COL, 'span'),
        Output(IDs.PLOTS_COL, 'span'),
        Input(IDs.COLLAPSE_COMMENTS_ICON, 'n_clicks'),
        State(IDs.COMMENT_STORE, 'data'),
        State(IDs.SELECTED_PLOT_ID_STORE, 'data'),
        State(IDs.COMMENTS_COL, 'span'),
        config_prevent_initial_callbacks=True
)
def collapse_comments(n_clicks, comments: dict, selected_plot_id: str, span: int):
    if span == 3:
        plot_col_span = 11
        comments_col_span = 1
        return [create_comments_section_open_icon], comments_col_span, plot_col_span
    else:
        plot_col_span = 9
        comments_col_span = 3
        comments = [Comment(**cmt) for cmt in comments[selected_plot_id]]
        return create_comments_section(selected_plot_id, comments), comments_col_span, plot_col_span


@dash.callback(
        Output(IDs.PLOTS_COL, 'children', allow_duplicate=True),
        Input({'type': IDs.NEW_BLOCK_BTN, 'index': ALL}, 'n_clicks'),
        State(IDs.PLOTS_COL, 'children'),
        config_prevent_initial_callbacks=True
)
def add_textarea(n_clicks, children):
    add_textarea_btn_id = ctx.triggered_id
    patched_children = Patch()

    insert_ind = find_add_text_block_btn(children, add_textarea_btn_id)
    new_text_block = create_textblock()
    patched_children.insert(insert_ind, new_text_block)
    return patched_children


dash.clientside_callback("""
(id) => {
  function stringifyId(id) {
    if (typeof id !== "object") {
      return id;
    }
    const stringifyVal = (v) => (v && v.wild) || JSON.stringify(v);
    const parts = Object.keys(id)
      .sort()
      .map((k) => JSON.stringify(k) + ":" + stringifyVal(id[k]));
    return "{" + parts.join(",") + "}";
  }
  setTimeout(() => {
    var ta = document.getElementById(stringifyId(id))
    ta.addEventListener('contextmenu', (e) => {
      dash_clientside.set_props(id, {disabled: false})
      setTimeout(() => ta.focus(), 100)
      e.preventDefault()
    })
    ta.addEventListener('blur', () => {dash_clientside.set_props(id, {disabled: true})})
  }, 300)
  return dash_clientside.no_update
  }
""",
Output({'type': IDs.PLOT_BLOCK_TEXTAREA, 'index': MATCH, 'num': MATCH}, 'id'),
Input({'type': IDs.PLOT_BLOCK_TEXTAREA, 'index': MATCH, 'num': MATCH}, 'id')
)
