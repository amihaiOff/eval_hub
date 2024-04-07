import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify
from plotly.io import from_json

from helpers import create_user_avatar
from report_data_classes import (
    ReportData,
    GraphBlock,
    Comment,
    GraphParameters,
    GraphData
)
from names import IDs



SOME_TEXT = "In the sprawling expanse of the universe, our tiny blue planet Earth is but a speck of dust. Yet, upon this minuscule orb, the dance of life unfolds in magnificent complexity. From the depths of the oceans to the peaks of the tallest mountains, life thrives in all its diversity. Each organism, from the tiniest bacterium to the mightiest whale, plays its part in the intricate web of existence."


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


def create_graph_params_text(graph_parameters: GraphParameters):
    children = []
    for name, value in graph_parameters.items():
        children.extend([html.Span(f'{name}: ', style={'font-weight': 'bold'}), value, html.Br()])

    return html.P(children)


def create_graph_block(title: str,
                       graph_parameters: GraphParameters,
                       description: str,
                       graph_data: GraphData,
                       graph_block_id: str):
    return dmc.Stack([
        dmc.Group([
            dmc.Title(title, order=2, color='gray', align='center',
                      style={'margin-bottom': '0.5rem'}),
            dmc.ActionIcon(
                    DashIconify(icon="carbon:close", color='gray', width=30),
                    size='xl',
                    id={'type': 'close_btn', 'index': graph_block_id}
            )
        ], position='apart'),
        dmc.Group([
            dmc.ActionIcon(DashIconify(icon='lucide:expand', color='gray', width=20),
                           id={'type': IDs.PLOT_EXPAND, 'index': graph_block_id}),
            dmc.Accordion([
                dmc.AccordionItem([
                    dmc.AccordionControl('Parameters', style={'color': 'gray', 'padding': 0, 'border-bottom': 'none'}),
                    dmc.AccordionPanel([
                        create_graph_params_text(graph_parameters)
                    ], style={'color': 'gray'})
                ], value='parameters', style={'border-bottom': 'none'}),
            ], chevronPosition='left', style={'width': '30%', 'margin-bottom': '0'})
        ]),
        dmc.Text(description, color='gray', size='md', weight=400, align='left'),
        dcc.Graph(figure=from_json(graph_data)),
        dmc.Modal(dcc.Graph(figure=from_json(graph_data)),
                  id={'type': IDs.FULL_SCREEN_MODAL, 'index': graph_block_id},
                  opened=False,
                  title='Full screen',
                  withCloseButton=True,
                  styles={'modal': {'width': '80vw', 'height': '70vh'}})

    ], style={'margin-top': '1rem',
              'padding-bottom': '1rem',
              'width': '100%'}
    )


def create_comment(comment: Comment):
    return dmc.Stack([
        dmc.Group([
            create_user_avatar(comment.user, size='sm'),
            dmc.Text(comment.user, color='gray', size='md', weight=700, align='left')
        ]),
        dmc.Text(comment.comment_text, color='gray', size='md', weight=400, align='left')
    ], style={'margin-bottom': '1rem'})


def create_comment_input(graph_block_id: str):
    return dmc.Textarea(
            id={'type': IDs.COMMENT_INPUT, 'index': graph_block_id},
            placeholder='Write a comment...',
            label='',
            radius='md',
            rightSection=dmc.ActionIcon(
                    DashIconify(icon='material-symbols-light:send', color='gray', width=20),
                    id={'type': IDs.COMMENT_SUBMIT, 'index': graph_block_id},
                    size='xl'
            ),
            rightSectionWidth=50
    )


def create_comment_card(comments: list[Comment], graph_block_id: str):
    return dmc.Card([
       dmc.CardSection([
           dmc.Group([
               dmc.Text('Discussion', color='gray', size='md', weight=400, align='left'),
               dmc.ActionIcon(
                       DashIconify(icon="lucide:expand"),
                       color="gray",
                       variant="transparent",
                )],
               position="apart"),
       ],
           withBorder=True,
           inheritPadding=True,
           py="xs",
       ),
       dmc.Stack([create_comment(cmt) for cmt in comments],
                 id={'type': IDs.COMMENT_STACK, 'index': graph_block_id},
                 style={'overflow-y': 'auto', 'height': '500px', 'margin-bottom': '1rem'}),

       create_comment_input(graph_block_id)
    ], radius='lg', withBorder=False, style={'height': '100%'}
    )


def create_graph_comment_block(graph_block: GraphBlock):
    return dmc.Grid([
        dmc.Col([
            create_graph_block(graph_block.title,
                               graph_block.graph_parameters,
                               graph_block.description,
                               graph_block.graph_data,
                               graph_block.id),
        ], span=8),
        dmc.Col([
            create_comment_card(graph_block.comments, graph_block.id)
        ], span='auto', style={'height': '100%'})
    ], gutter='xs', style={'height': '700px', 'margin-bottom': '50px'}
    )


def create_page_content(report_data: ReportData):
    stack = [create_report_header(report_data.title, report_data.description)]

    for graph_block in report_data.graph_blocks:
        stack.append(create_graph_comment_block(graph_block))

    return dmc.Stack(stack)
