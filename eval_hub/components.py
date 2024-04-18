import random
from typing import List

from dash.development.base_component import Component
import dash_mantine_components as dmc
import dash_summernote as dsn
from dash import html
from dash_iconify import DashIconify

from eval_hub.names import IDs


def _create_login_modal():
    with open('../dummy_data/users', 'r') as f:
        users = f.readlines()
        data = [{'label': user, 'value': user} for user in users]

    return dmc.Modal([
        dmc.Text('Please enter your username'),
        dmc.Space(h=20),
        dmc.Select(id=IDs.USERNAME_INPUT,
                   data=data,
                   placeholder='Username',
                   label='Username'),
        dmc.Space(h=20),
        dmc.Group([
            dmc.Button('Login',
                       id=IDs.LOGIN_MODAL_LOGIN,
                       color='blue'),
        ], position='right')
    ],
            id=IDs.LOGIN_MODAL,
            title='Login',
            opened=True,
            withCloseButton=False,
            closeOnEscape=False,
            closeOnClickOutside=False
)


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


def create_textblock() -> html.Div:
    """
    Create a text block to add to the report
    :return:
    """
    return html.Div([dsn.DashSummernote(
            toolbar=[
                ["style", ["style"]],
                ["font", ["bold", "underline", "clear"]],
                ["fontname", ["fontname"]],
                ["para", ["ul", "ol", "paragraph"]],
                ["table", ["table"]],
                ["insert", ["link", "picture", "video"]],
                ["view", ["fullscreen", "codeview"]]
            ],
    )
    ], style={'width': '80%', 'margin-left': '5rem', 'margin-top': '1rem', 'margin-bottom': '1rem'},
            id={'type':  IDs.PLOT_BLOCK_TEXTAREA,
                'index': random.randint(0, 1000)}
    )


def create_comments_section_open_icon():
    return dmc.ActionIcon(DashIconify(icon='pajamas:collapse-left',
                                      color='gray',
                                      width=20),
                          id=IDs.COLLAPSE_COMMENTS_ICON)


def create_add_text_block_button():
    return dmc.Tooltip([
        dmc.Button('+',
                   variant='outline',
                   className='new-block',
                   size='lg',
                   radius='xl',
                   id={'type': IDs.NEW_BLOCK_BTN, 'index': random.randint(0, 200)}
                   )
    ],
            label='New text block',
            openDelay=200,
            withArrow=True,
            position='left',
            id={'type': IDs.NEW_BLOCK_BTN_TOOLTIP, 'index': random.randint(0, 200)}
            )


def create_new_block(title: str, block_ind: int, children: List[Component]):
    return dmc.AccordionMultiple([
            dmc.AccordionItem([
                dmc.AccordionControl([
                    dmc.Group([
                        dmc.Title(title, order=2, color='gray', align='left', style={'margin-bottom': '0'}),
                        dmc.ActionIcon(DashIconify(icon='carbon:close', color='gray', width=20),
                                       id={'type': IDs.DELETE_BLOCK_ICON, 'index': block_ind})
                    ])
                ], className='block-title'),
                dmc.AccordionPanel(children,
                                   id={'type': IDs.BLOCK_CONTENT, 'index': block_ind})
            ], style={'border-bottom': 'none'})
        ],
            value=[title],
            className='block',
            id={'type': IDs.PLOT_BLOCK, 'index': block_ind}
    )
