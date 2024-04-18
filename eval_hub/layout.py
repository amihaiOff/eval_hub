from typing import List

import dash_mantine_components as dmc
from dash import dcc, html
from dash.development.base_component import Component
from dash_iconify import DashIconify
from plotly.io import from_json

from eval_hub.components import create_add_text_block_button, create_new_block, create_textblock
from eval_hub.names import IDs
from eval_hub.report_data_classes import GraphData, GraphParameters
from eval_hub.utils import create_graph_params_text
from helpers import create_user_avatar
from report_data_classes import (
    PlotBlock,
    TextBlock,
    ReportData,
    Comment,
    GraphParameters,
    GraphData
)
from names import IDs


def create_left_header():
    return dmc.Grid([
        create_user_avatar('dummy user', size='lg'),  # todo: replace with actual user
        dmc.Stack([
            dmc.Text("Rappi eval", weight=700, size="xl", style={"margin-bottom": "0.1"}),
            dmc.Text("Amihai", weight=300, size="l", style={"margin-top": "0.1"}),
        ], style={"margin-left": "1rem", "gap": "2px"}, spacing="xs")
    ], style={'margin-top': '1rem', 'border-bottom': '1px solid lightgray', 'padding-bottom': '1rem', 'width': '100%'})


def create_folder_header():
    return dmc.Group([
        DashIconify(icon='bi:folder-fill', color='gray', width=30),
        dmc.Title('Rappi', order=2, color='gray')
    ])


def create_available_reports():
    return dmc.Stack([
        dmc.Group([
            DashIconify(icon='bi:file-earmark-text-fill', color='gray', width=20),
            dmc.Title('Rappi eval', order=3, color='gray')
        ]),
        dmc.Group([
            DashIconify(icon='bi:file-earmark-text-fill', color='gray', width=20),
            dmc.Title('Rappi buyers eval', order=3, color='gray')
        ]),
    ], style={'margin-left': '1rem'}
    )


def create_left_panel():
    return dmc.Stack([
        create_left_header(),
        dmc.Space(h=50),
        create_folder_header(),
        create_available_reports()

    ], style={'background': '#FBFBFA', 'border-right': '1px solid gray', 'height': '100vh'})


def create_report_header(title: str, description: str):
    return dmc.Stack([
        dmc.Title(title, order=1, color='gray', align='center',
                  style={'margin-bottom': '1rem', 'font-size': 'xxx-large'}),
        dmc.Text(description, color='gray', size='md', weight=400)
    ], style={'margin-top': '1rem', 'border-bottom': '1px solid lightgray', 'padding-bottom': '1rem', 'width': '100%'}
    )


def create_graph_block(title: str,
                       graph_parameters: GraphParameters,
                       description: str,
                       graph_data: GraphData,
                       graph_block_id: str,
                       block_ind: int):

    return
    # return dmc.Stack([
    #     dmc.AccordionMultiple([
    #         dmc.AccordionItem([
    #             dmc.AccordionControl(dmc.Title(title, order=2, color='gray', align='left', style={'margin-bottom': '0'}),
    #                                  className='block-title'
    #                                  ),
    #             dmc.AccordionPanel([
    #                 dmc.Group([
    #                     dmc.HoverCard([
    #                         dmc.HoverCardTarget([
    #                             DashIconify(icon='jam:settings-alt', color='gray', width=20),
    #                         ]),
    #                         dmc.HoverCardDropdown([
    #                             create_graph_params_text(graph_parameters)
    #                         ]),
    #                     ], withArrow=True, position='right', shadow='md'),
    #                     dmc.Group([
    #                         dmc.ActionIcon(
    #                                 DashIconify(icon="mdi:comments-text", color='gray', width=30),
    #                                 size='xl',
    #                                 id={'type': IDs.COMMENT_ICON, 'index': graph_block_id}
    #                         ),
    #                         dmc.ActionIcon(
    #                                 DashIconify(icon="carbon:close", color='gray', width=30),
    #                                 size='xl',
    #                                 id={'type': IDs.DELETE_PLOT_BLOCK_ICON, 'index': graph_block_id}
    #                         )
    #                     ], position='right')
    #
    #                 ], position='apart'),
    #
    #                 dmc.Text(description, color='gray', size='md', weight=400, align='left'),
    #                 dcc.Graph(figure=from_json(graph_data)),
    #
    #             ], id={'type': IDs.BLOCK_CONTENT, 'index': graph_block_id})
    #         ], value=title, style={'border-bottom': 'none'})
    #     ], value=[title]),
    # ], style={'margin-top': '1rem',
    #           'padding-bottom': '1rem',
    #           'width': '100%'},
    #    id={'type': IDs.PLOT_BLOCK, 'index': graph_block_id}
    # )


def create_comment(comment: Comment):
    return dmc.Stack([
        dmc.Group([
            create_user_avatar(comment.user, size='sm'),
            dmc.Text(comment.user, color='gray', size='md', weight=700, align='left')
        ]),
        dmc.Text(comment.comment_text, color='gray', size='md', weight=400, align='left')
    ], style={'margin-bottom': '1rem'})


def create_comment_input():
    return dmc.Textarea(
            id=IDs.COMMENT_INPUT,
            placeholder='Write a comment...',
            label='',
            radius='md',
            rightSection=dmc.ActionIcon(
                    DashIconify(icon='material-symbols-light:send', color='gray', width=20),
                    id=IDs.COMMENT_SUBMIT,
                    size='xl'
            ),
            rightSectionWidth=50
    )


def create_comments_section(title: str, comments: List[Comment]):
    return dmc.Stack([
        dmc.ActionIcon(DashIconify(icon='pajamas:collapse-right', color='gray', width=20),
                       style={'margin-bottom': '0'},
                       id=IDs.COLLAPSE_COMMENTS_ICON),
        dmc.Title(title,
                  order=2,
                  color='gray',
                  align='center',
                  id=IDs.COMMENTS_SECTION_TITLE),
        dmc.Stack([create_comment(cmt) for cmt in comments], id=IDs.COMMENTS_STACK),
        create_comment_input()
    ], spacing='xs')


def create_page_content(report_data: ReportData):
    plot_stack = []
    for i, block in enumerate(report_data.blocks):
        if isinstance(block, PlotBlock):
            block_contents = create_plot_block(block.graph_parameters,
                                               block.graph_data,
                                               block.description,
                                               block.id)
            plot_stack.append(create_new_block(block.title,
                                               block_ind=i,
                                               children=block_contents))

        elif isinstance(block, TextBlock):
            block_contents = create_textblock(text=block.text,
                                              block_ind=i)
            plot_stack.append(create_new_block(title="",
                                               block_ind=i,
                                               children=block_contents))

        plot_stack.append(create_add_text_block_button())

    first_plot_block: PlotBlock = report_data.get_first_plot_block()
    main_grid = dmc.Grid([
        dmc.Col(plot_stack,
                span=9,
                className='app-column',
                id=IDs.PLOTS_COL,
                style={'border-right': '1px solid lightgray'}),
        dmc.Col([create_comments_section(first_plot_block.title,
                                         first_plot_block.comments)],
                span=3,
                style={'overflow-y': 'auto', 'height': '100vh'},
                className='app-column',
                id=IDs.COMMENTS_COL)
    ])

    header = create_report_header(report_data.title, report_data.description)
    page_stack = [header, main_grid]
    return dmc.Stack(page_stack)


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
) -> dmc.HoverCard:
    return dmc.HoverCard([
        dmc.HoverCardTarget([
            DashIconify(icon='jam:settings-alt', color='gray', width=20),
        ]),
        dmc.HoverCardDropdown([
            create_graph_params_text(graph_parameters)
        ]),
    ], withArrow=True, position='right', shadow='md')


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
